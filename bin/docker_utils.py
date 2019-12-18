#!/usr/bin/env python

from __future__ import print_function
from json import loads
from os.path import dirname, abspath
from requests import request
from os.path import expanduser
from requests.exceptions import HTTPError
import os, glob, sys

DOCKER_REGISTRY_API='https://registry-1.docker.io/v2'
DOCKER_HUB_API='https://hub.docker.com/v2'
DOCKER_HUB_TOKEN = None

def hub_request(uri, data=None, params=None, headers=None, method='GET', dryrun=False, json=False):
  global DOCKER_HUB_TOKEN
  if not DOCKER_HUB_TOKEN:
    DOCKER_HUB_TOKEN = get_token()
  if not headers: headers = {}
  headers['Authorization'] = 'JWT %s' % DOCKER_HUB_TOKEN
  if dryrun: 
    return('Dry run mode enabled, no changes to Docker Hub applied')
  else:
    return http_request('%s%s' %(DOCKER_HUB_API, uri), data, params, headers, method, json)

def http_request(url, data=None, params=None, headers=None, method = 'GET', json=False):
  response = request(method=method, url=url, data=data,  params=params, headers=headers)
  if not response.ok:
    return response
  return response.json() if json else response

# get token for docker Registry API
def get_registry_token(repo):
  uri = 'https://auth.docker.io/token'
  payload = {
    'service' : 'registry.docker.io',
    'scope' : 'repository:%s:pull' % repo
  }
  return http_request(uri, params = payload, json = True)['token']

# get token for Docker HUB API:
def get_token(filepath=expanduser("~/.docker-token")):
  uri = '%s/users/login/' % DOCKER_HUB_API
  secret = open(filepath).read().strip()
  return http_request(uri, loads(secret), method = 'POST', json=True)['token']

def get_repos(username, page_size=500):
  uri = '/repositories/%s/' % username
  payload = {"page_size" : page_size}
  response = hub_request(uri, params=payload, json=True)
  repos = []
  for repo in response['results']:
    repos.append(str(repo['name']))
  if repos == []: return 'No repositories found.\nCheck docker hub username'
  return repos

def create_repo(username, repo, dryrun=True, private=False):
  payload = {
    "namespace":"%s" % username,
    "name":"%s" % repo,
    "is_private":"%s" % private
  }
  response = hub_request("/repositories/", payload, method = 'POST', dryrun=dryrun)
  return response if dryrun else response.content

def delete_repo(username, repo, dryrun=True):
  uri = '/repositories/%s/%s' % (username, repo)
  response = hub_request(uri, method = 'DELETE', dryrun=dryrun)
  return response if dryrun else (response, response.reason)

def get_members(username, teamname):
  uri = '/orgs/%s/groups/%s/members/' % (username, teamname)
  response = hub_request(uri, json=True)
  members = []
  for member in response:
    try: members.append(str(member['username']))
    except TypeError:
      return response, response.reason
  return members

def add_member(username, teamname, member, dryrun=True):
  uri = '/orgs/%s/groups/%s/members/' % (username, teamname)
  data = {"member":"%s" % member}
  response = hub_request(uri, data=data, method = 'POST', dryrun=dryrun)
  return response if dryrun else (response.ok, response, response.reason, response.content)

def delete_member(username, teamname, member, dryrun=True):
  uri = '/orgs/%s/groups/%s/members/%s/' % (username, teamname, member)
  response = hub_request(uri, method = 'DELETE', dryrun=dryrun)
  return response if dryrun else (response, response.reason)

def get_teams(username, page_size=500):
  uri = '/orgs/%s/groups/' % username
  payload = {"page_size" : page_size}
  response = hub_request(uri, params=payload, json=True)
  teams = {}
  try: response['results']
  except TypeError:
    return response, response.content
  for team in response['results']:
    key = str(team['name'])
    value = str(team['id'])
    teams[key] = value
  return teams

def create_team(username, teamname, dryrun=True):
  uri = '/orgs/%s/groups/' % username
  data = {"name":"%s" % teamname}
  response = hub_request(uri, data=data, method = 'POST', dryrun=dryrun)
  return response if dryrun else (response, response.content)

def delete_team(username, teamname, dryrun=True):
  uri = '/orgs/%s/groups/%s' % (username, teamname)
  response = hub_request(uri, method = 'DELETE', dryrun=dryrun)
  return response if dryrun else (response, response.reason)

def get_permissions(username, teamname):
  uri = '/orgs/%s/groups/%s/repositories/' % (username, teamname)
  headers = {}
  response = hub_request(uri, headers, json=True)
  return response

# permissions must be: 'read' / 'write' / 'admin'
def add_permissions(username, repo, group_id, permission, dryrun=True):
  uri = '/repositories/%s/%s/groups/' % (username, repo)
  payload = {
    "group_id" : "%s" % group_id,
    "permission" : "%s" % permission
  }
  response = hub_request(uri, data=payload, method = 'POST', dryrun=dryrun)
  return response if dryrun else (response, response.content)

def delete_permissions(username, repo, group_id, dryrun=True):
  uri = '/repositories/%s/%s/groups/%s' % (username, repo, group_id)
  response = hub_request(uri, method = 'DELETE', dryrun=dryrun)
  return response if dryrun else (response, response.reason)

def get_tags(image, page_size=500):
  uri = '/repositories/%s/tags' % image
  payload = {"page_size" : page_size}
  response = hub_request(uri, params=payload, json=True)
  tags = []
  for tag in response['results']:
    tags.append(str(tag['name']))
  return tags

def delete_tag(repo, tag, dryrun=True):
  print('** Deleting tag: %s from %s repository....'% (tag, repo))
  uri = '/repositories/%s/tags/%s/' % (repo, tag)
  response = hub_request(uri, method = 'DELETE', dryrun=dryrun)
  return response if dryrun else (response, response.reason)

def logout():
  uri = '/logout/'
  return hub_request(uri, method='POST', json=True)['detail']

def get_digest_of_image(repo, tag):
  uri = '/repositories/%s/tags/%s' % (repo, tag)
  try:
    return hub_request(uri, json=True)['images'][0]['digest'].split(":")[-1]
  except TypeError:
    return hub_request(uri)

def get_manifest(image):
  repo = image.split(":",1)[0]
  if '/' not in repo:
    repo = 'library/'+repo
  tag = image.split(":",1)[-1]
  if repo==tag: tag="latest"
  url = '%s/%s/manifests/%s' % (DOCKER_REGISTRY_API, repo, tag)
  token = get_registry_token(repo)
  headers = {}
  headers['Authorization'] = 'Bearer %s' % token
  return http_request(url, None, None, headers, json=True)

def has_parent_changed(parent, image):
  image_manifest = get_manifest(image)
  try: image_manifest['fsLayers']
  except KeyError:
    if image_manifest[u'errors'][0][u'code'] == 'MANIFEST_UNKNOWN':
      return True
    else:
      raise Exception(image_manifest)
  parent_layers = get_manifest(parent)['fsLayers']
  image_layers = image_manifest['fsLayers']
  while parent_layers and image_layers:
    if parent_layers.pop()!=image_layers.pop():
      return True
  return len(parent_layers)>0
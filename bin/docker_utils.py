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

def hub_request(uri, data=None, params=None, headers=None, method = 'GET', json=False):
  global DOCKER_HUB_TOKEN
  if not DOCKER_HUB_TOKEN:
    DOCKER_HUB_TOKEN = get_token()
  if not headers: headers = {}
  headers['Authorization'] = 'JWT %s' % DOCKER_HUB_TOKEN
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
def get_token():
  uri = '%s/users/login/' % DOCKER_HUB_API
  secret = open(expanduser("~/.docker-token")).read().strip()
  return http_request(uri, loads(secret), method = 'POST', json=True)['token']

def get_repos(user):
  uri = '/repositories/%s/' % user
  payload = {
    "page_size" : 500,
  }
  response = hub_request(uri, params=payload, json=True)
  repos = []
  try: response['results']
  except TypeError:
    return response, response.reason
  for repo in response['results']:
    repos.append(str(repo['name']))
  return repos

def create_repo(user, repo, private=False):
  payload = {
    "namespace":"%s" % user,
    "name":"%s" % repo,
    "is_private":"%s" % private
  }
  return hub_request("/repositories/", payload, method = 'POST').content

def delete_repo(user, repo):
  uri = '/repositories/%s/%s' % (user, repo)
  response = hub_request(uri, method = 'DELETE')
  return response, response.reason

def get_members(orgname, teamname):
  uri = '/orgs/%s/groups/%s/members/' % (orgname, teamname)
  response = hub_request(uri, json=True)
  members = []  
  for member in response:
    try: members.append(str(member['username']))
    except TypeError:
      return response, response.reason
  return members

def add_member(orgname, teamname, member):
  uri = '/orgs/%s/groups/%s/members/' % (orgname, teamname)
  data = {"member":"%s" % member}
  response = hub_request(uri, data=data, method = 'POST')
  return response, response.reason, response.content

def delete_member(orgname, teamname, member):
  uri = '/orgs/%s/groups/%s/members/%s/' % (orgname, teamname, member)
  response = hub_request(uri, method = 'DELETE')
  return response, response.reason

def get_teams(orgname):
  uri = '/orgs/%s/groups/' % orgname
  response = hub_request(uri)
  teams = {}
  try: response.json()['results']
  except KeyError:
    return response, response.content
  for team in response.json()['results']:
    key = str(team['name'])
    value = str(team['id'])
    teams[key] = value
  return teams

def create_team(orgname, teamname):
  uri = '/orgs/%s/groups/' % orgname
  data = {"name":"%s" % teamname}
  response = hub_request(uri, data=data, method = 'POST')
  return response, response.content

def delete_team(orgname, teamname):
  uri = '/orgs/%s/groups/%s' % (orgname, teamname)
  response = hub_request(uri, method = 'DELETE')
  return response, response.reason

# permissions must be: 'read' / 'write' / 'admin'
def add_permissions(orgname, repo, group_id, permission):
  uri = '/repositories/%s/%s/groups/' % (orgname, repo)
  payload = {
    "group_id" : "%s" % group_id,
    "permission" : "%s" % permission
  }
  response = hub_request(uri, data=payload, method = 'POST')
  return response, response.content

def delete_permissions(orgname, repo, group_id):
  uri = '/repositories/%s/%s/groups/%s' % (orgname, repo, group_id)
  response = hub_request(uri, method = 'DELETE')
  return response, response.reason

def deleteTag(repo, tag, dryRun):
  print('** Deleting tag: %s from %s repository....'% (tag, repo))
  if dryRun: return 'Dry Run mode is ON, no tags deleted'
  uri = '/repositories/%s/tags/%s/' % (repo, tag)
  response = hub_request(uri, method = 'DELETE')
  return response, response.reason

def logout():
  uri = '/logout/'
  return hub_request(uri, method='POST').content

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

def tags(image):
  uri = '/repositories/%s/tags' % image
  payload = {
    "page_size" : 500,
  }
  response = hub_request(uri, params=payload, json=True)
  tags = []
  for tag in response['results']:
    tags.append(str(tag['name']))
  return tags

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

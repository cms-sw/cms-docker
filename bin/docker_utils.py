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

def http_request(url, data=None, headers=None, method = 'GET', json=False):
  response = request(method=method, url=url, data=data, headers=headers)
  if not response.ok:
    return response
  return response.json() if json else response

# get token for docker Registry API
def get_docker_token(repo):
  return http_request('https://auth.docker.io/token?service=registry.docker.io\
&scope=repository:%s:pull' % repo, json=True)['token']

# get token for Docker HUB API:
def get_dockerHubToken(DOCKER_HUB_API):
  url = '%s/users/login/' % DOCKER_HUB_API
  secret = open(expanduser("~/.docker-token")).read().strip()
  response = http_request(url, loads(secret), method = 'POST', json=True)
  return response['token']

def get_repos(DOCKER_HUB_API, user):
  url = '%s/repositories/%s/' % (DOCKER_HUB_API, user)
  response = http_request(url, json=True)
  repos = []
  try: response['results']
  except TypeError:
    return response, response.reason
  for repo in response['results']:
    repos.append(str(repo['name']))
  return repos

def create_repo(DOCKER_HUB_API, token, user, repo, private=False):
  url = '%s/repositories/' % DOCKER_HUB_API
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  payload = {
    "namespace":"%s" % user,
    "name":"%s" % repo,
    "is_private":"%s" % private
  }
  response = http_request(url, payload, headers, method = 'POST')
  return response.content

def delete_repo(DOCKER_HUB_API, user, repo, token):
  url = '%s/repositories/%s/%s' % (DOCKER_HUB_API, user, repo)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, headers=headers, method = 'DELETE')
  return response, response.reason

def get_members(DOCKER_HUB_API, orgname, teamname, token):
  url = '%s/orgs/%s/groups/%s/members/' % (DOCKER_HUB_API, orgname, teamname)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, headers=headers, json=True)
  members = []  
  for member in response:
    try: members.append(str(member['username']))
    except TypeError:
      return response
  return members

def add_member(DOCKER_HUB_API, orgname, teamname, token, member):
  url = '%s/orgs/%s/groups/%s/members/' % (DOCKER_HUB_API, orgname, teamname)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  data = {"member":"%s" % member}
  response = http_request(url, data=data, headers=headers, method = 'POST')
  return response, response.reason

def delete_member(DOCKER_HUB_API, orgname, teamname, member, token):
  url = '%s/orgs/%s/groups/%s/members/%s/' % (DOCKER_HUB_API, orgname, teamname, member)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, headers=headers, method = 'DELETE')
  return response, response.reason

def get_teams(DOCKER_HUB_API, orgname, token):
  url = '%s/orgs/%s/groups/' % (DOCKER_HUB_API, orgname)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, headers=headers)
  teams = {}
  try: response.json()['results']
  except KeyError:
    return response, response.content
  for team in response.json()['results']:
    key = str(team['name'])
    value = str(team['id'])
    teams[key] = value
  return teams

def create_team(DOCKER_HUB_API, orgname, token, teamname):
  url = '%s/orgs/%s/groups/' % (DOCKER_HUB_API, orgname)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  data = {"name":"%s" % teamname}
  response = http_request(url, data=data, headers=headers, method = 'POST')
  return response, response.content

def delete_team(DOCKER_HUB_API, orgname, teamname, token):
  url = '%s/orgs/%s/groups/%s' % (DOCKER_HUB_API, orgname, teamname)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, headers=headers, method = 'DELETE')
  return response, response.reason

# permissions must be: 'read' / 'write' / 'admin'
def add_permissions(DOCKER_HUB_API, orgname, repo, group_id, token, permission):
  url = '%s/repositories/%s/%s/groups/' % (DOCKER_HUB_API, orgname, repo)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  payload = {"group_id" : "%s" % group_id, "permission" : "%s" % permission}
  response = http_request(url, data=payload, headers=headers, method = 'POST')
  return response, response.content

def delete_permissions(DOCKER_HUB_API, orgname, repo, group_id, token):
  url = '%s/repositories/%s/%s/groups/%s' % (DOCKER_HUB_API, orgname, repo, group_id)
  headers = {}
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, headers=headers, method = 'DELETE')
  return response, response.reason

def deleteTag(token, repo, tag, dryRun):
  print('** Deleting tag: %s from %s repository....'% (tag, repo))
  if dryRun: return {}
  url = '%s/repositories/%s/tags/%s/' % (DOCKER_HUB_API, repo, tag)
  headers = {}
  headers['Accept'] = 'application/json'
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, None, headers, method = 'DELETE')
  return response, response.reason

def logout(token):
  url = '%s/logout/' % DOCKER_HUB_API
  headers = {}
  headers['Accept'] = 'application/json'
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, None, headers, method='POST')
  return response.content

def get_digest_of_image(repo, tag):
  url = '%s/repositories/%s/tags/%s' % (DOCKER_HUB_API, repo, tag)
  try:
    return http_request(url, json=True)['images'][0]['digest'].split(":")[-1]
  except TypeError:
    return http_request(url)

def get_manifest(image):
  repo = image.split(":",1)[0]
  if '/' not in repo:
    repo = 'library/'+repo
  tag = image.split(":",1)[-1]
  if repo==tag: tag="latest"
  url = '%s/%s/manifests/%s' % (DOCKER_REGISTRY_API, repo, tag)
  token = get_docker_token(repo)
  headers = {}
  headers['Authorization'] = 'Bearer %s' % token
  response = http_request(url, None, headers, json=True)
  return response

def get_tags(image):
  token = get_docker_token(image)
  headers = {}
  headers['Authorization'] = 'Bearer %s' % token
  url = '%s/%s/tags/list?n=500' % (DOCKER_REGISTRY_API, image)
  response = http_request(url, None, headers, json=True)
  try: return response['tags']
  except TypeError: return response

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

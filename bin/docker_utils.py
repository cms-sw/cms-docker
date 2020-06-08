#!/usr/bin/env python

from __future__ import print_function
from json import loads
from os.path import dirname, abspath, join
from requests import request
from os.path import expanduser
from requests.exceptions import HTTPError
import os, glob
import yaml

DOCKER_REGISTRY_API='https://registry-1.docker.io/v2'
DOCKER_HUB_API='https://hub.docker.com/v2'
DOCKER_HUB_TOKEN = None

def hub_request(uri, data=None, params=None, headers=None, method='GET', json=False):
  global DOCKER_HUB_TOKEN
  if not DOCKER_HUB_TOKEN:
    DOCKER_HUB_TOKEN = get_token()
  if not headers: headers = {}
  headers['Authorization'] = 'JWT %s' % DOCKER_HUB_TOKEN
  return http_request('%s%s' %(DOCKER_HUB_API, uri), data, params, headers, method, json)

def http_request(url, data=None, params=None, headers=None, method = 'GET', json=False):
  response = request(method=method, url=url, data=data,  params=params, headers=headers)
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
  response = http_request(uri, loads(secret), method = 'POST', json=True)
  try: return response['token']
  except: return response

def get_repos(username, page_size=500):
  uri = '/repositories/%s/' % username
  payload = {"page_size" : page_size}
  response = hub_request(uri, params=payload, json=True)
  repos = []
  try:
    for repo in response['results']:
      repos.append(str(repo['name']))
  except: return (False, response)
  return (True, repos)

def create_repo(username, repo, private=False):
  payload = {
    "namespace":"%s" % username,
    "name":"%s" % repo,
    "is_private":"%s" % private
  }
  response = hub_request("/repositories/", payload, method = 'POST')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def delete_repo(username, repo, force=False):
  uri = '/repositories/%s/%s' % (username, repo)
  if force or not get_tags('%s/%s'%(username,repo))[1]:
    response = hub_request(uri, method = 'DELETE')
    return (False, response, response.reason, response.text) if not response.ok else (response.ok,)
  else: return False

def get_members(username, teamname):
  uri = '/orgs/%s/groups/%s/members/' % (username, teamname)
  response = hub_request(uri, json=True)
  members = []
  try:
    for member in response:
      members.append(str(member['username']))
  except: return (False, response)
  return (True, members)

def add_member(username, teamname, member):
  uri = '/orgs/%s/groups/%s/members/' % (username, teamname)
  data = {"member":"%s" % member}
  response = hub_request(uri, data=data, method = 'POST')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def delete_member(username, teamname, member):
  uri = '/orgs/%s/groups/%s/members/%s/' % (username, teamname, member)
  response = hub_request(uri, method = 'DELETE')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def get_teams(username, page_size=500):
  uri = '/orgs/%s/groups/' % username
  payload = {"page_size" : page_size}
  response = hub_request(uri, params=payload, json=True)
  teams = {}
  try:
    for team in response['results']:
      key = str(team['name'])
      value = str(team['id'])
      teams[key] = value
  except: return (False, response)
  return (True, teams)

def create_team(username, teamname):
  uri = '/orgs/%s/groups/' % username
  data = {"name":"%s" % teamname}
  response = hub_request(uri, data=data, method = 'POST')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def delete_team(username, teamname, force=False):
  uri = '/orgs/%s/groups/%s' % (username, teamname)
  if force or not get_members(username, teamname)[1]:
    response = hub_request(uri, method = 'DELETE')
    return (False, response, response.reason, response.text) if not response.ok else (response.ok,)
  else: return False

def get_permissions(username, teamname):
  uri = '/orgs/%s/groups/%s/repositories/' % (username, teamname)
  headers = {}
  response = hub_request(uri, headers, json=True)
  permissions = {}
  try:
    for permission in response:
      permissions[permission['repository']] = permission['permission']
  except: return (False, response)
  return (True, permissions)

# permissions must be: 'read' / 'write' / 'admin'
def add_permissions(username, repo, group_id, permission):
  uri = '/repositories/%s/%s/groups/' % (username, repo)
  payload = {
    "group_id" : "%s" % group_id,
    "permission" : "%s" % permission
  }
  response = hub_request(uri, data=payload, method = 'POST')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def delete_permissions(username, repo, group_id):
  uri = '/repositories/%s/%s/groups/%s' % (username, repo, group_id)
  response = hub_request(uri, method = 'DELETE')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def get_tags(image, page_size=500):
  uri = '/repositories/%s/tags' % image
  payload = {"page_size" : page_size}
  response = hub_request(uri, params=payload, json=True)
  tags = []
  try:
    for tag in response['results']:
      tags.append(str(tag['name']))
  except: return (False, response)
  return (True, tags)

def delete_tag(repo, tag):
  print('** Deleting tag: %s from %s repository....'% (tag, repo))
  uri = '/repositories/%s/tags/%s/' % (repo, tag)
  response = hub_request(uri, method = 'DELETE')
  return (False, response, response.reason, response.text) if not response.ok else (response.ok,)

def logout():
  uri = '/logout/'
  return hub_request(uri, method='POST', json=True)['detail']

def get_digest_of_image(repo, tag):
  uri = '/repositories/%s/tags/%s' % (repo, tag)
  try: return (True, hub_request(uri, json=True)['images'][0]['digest'].split(":")[-1])
  except: return (False, hub_request(uri).text)

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
      print("Image %s not found")
      return True
    else:
      raise Exception(image_manifest)
  parent_layers = get_manifest(parent)['fsLayers']
  image_layers = image_manifest['fsLayers']
  print("Layers: %s%s" % (parent,"\n  ".join([i['blobSum'] for i in parent_layers])))
  print("Layers: %s%s" % (image ,"\n  ".join([i['blobSum'] for i in image_layers])))
  while parent_layers and image_layers:
    if parent_layers.pop()!=image_layers.pop():
      return True
  return len(parent_layers)>0

def generate_yaml(username):
  teams_dict = {}
  repositories_dict = {}
  hub_teams = get_teams(username)
  if not hub_teams[0]:
    print(hub_teams[1])
    return False
  for team in hub_teams[1]:
    members_in_hub = get_members(username, team)[1]
    if members_in_hub == []: members_in_hub = None
    teams_dict[team] = members_in_hub
    if team != 'owners':
      permissions_for_repos = get_permissions(username, team)[1]
      repos_list = permissions_for_repos.keys()
      for repo in repos_list:
        team_access_pair = {}
        repo_permissions = {}
        team_access_pair[team] = permissions_for_repos[repo]
        repo_permissions[repo] = team_access_pair
        if next(iter(repo_permissions)) in repositories_dict.keys():
          repositories_dict[next(iter(repo_permissions))].update(next(iter(repo_permissions.values())))
        else:
          repositories_dict.update(repo_permissions)
  docker_config = dict.fromkeys(['repositories', 'teams'])
  docker_config['teams'] = teams_dict
  docker_config['repositories'] = repositories_dict
  logout()
  yaml_location = join(dirname(dirname(abspath(__file__))), 'generated-docker-config.yaml')
  with open(yaml_location, 'w') as file:
    yaml.safe_dump(docker_config, file, encoding='utf-8', allow_unicode=True, default_flow_style=False)
  return True

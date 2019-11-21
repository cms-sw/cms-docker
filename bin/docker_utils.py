#!/usr/bin/env python

from __future__ import print_function
from json import loads
from os.path import dirname, abspath
from requests import request
from os.path import expanduser
from urllib3.exceptions import HTTPError
import os, glob, sys

DOCKER_REGISTRY_API='https://registry-1.docker.io/v2/'
DOCKER_HUB_API='https://hub.docker.com/v2/'

def http_request(url, data=None, headers=None, method = 'GET', json=True):
  if data is None: data = {}
  if headers is None: headers = {}
  try:
    response = request(method=method, url=url, data=data, headers=headers)
    if response.status_code == 204:
      return {} if json else '{}'
    return loads(response.content) if json else response
  except HTTPError as error:
    if error.code == 401:
      return {} if json else '{}'
  return {} if json else '{}'

# get token for docker Registry API
def get_docker_token(repo):
  return http_request('https://auth.docker.io/token?service=registry.docker.io\
&scope=repository:%s:pull' % repo)['token']

# get token for Docker HUB API:
def get_dockerHubToken():
  url = '%susers/login/' % DOCKER_HUB_API
  docker_token = open(expanduser("~/.docker-token")).read().strip()
  data = loads(docker_token)
  response = http_request(url, data, None, method='POST')
  return response['token']

def deleteTag(token, repo, tag, dryRun):
  print('** Deleting tag: %s from %s repository....'% (tag, repo))
  if dryRun: return {}
  url = '%srepositories/%s/tags/%s/' % (DOCKER_HUB_API, repo, tag)
  headers = {}
  headers['Accept'] = 'application/json'
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, None, headers, method = 'DELETE')
  return response

def logout(token):
  url = '%slogout/' % DOCKER_HUB_API
  headers = {}
  headers['Accept'] = 'application/json'
  headers['Authorization'] = 'JWT %s' % token
  response = http_request(url, None, headers, method='POST')
  print(response)

def get_manifest(image):
  repo = image.split(":",1)[0]
  if '/' not in repo:
    repo = 'library/'+repo
  tag = image.split(":",1)[-1]
  if repo==tag: tag="latest"
  url = '%s%s/manifests/%s' % (DOCKER_REGISTRY_API, repo, tag)
  token = get_docker_token(repo)
  headers = {}
  headers['Authorization'] = 'Bearer %s' % token
  response = http_request(url, None, headers)
  return response

def get_tags(image):
  token = get_docker_token(image)
  headers = {}
  headers['Authorization'] = 'Bearer %s' % token
  url = '%s%s/tags/list?n=500' % (DOCKER_REGISTRY_API, image)
  response = http_request(url, None, headers)
  return response['tags']

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

#!/usr/bin/env python

from __future__ import print_function
from json import loads
import sys
import os, glob
from os.path import dirname, abspath
from get_image_config import get_docker_images
import json

if sys.version_info[0] == 2:
# python 2 module
  from commands import getstatusoutput as run_cmd
else:
# python 3 module
  from subprocess import getstatusoutput as run_cmd

def get_docker_token(repo):
  print('\nGetting docker.io token ....')
  e, o = run_cmd('curl --silent --request "GET" "https://auth.docker.io/token?service=registry.docker.io&scope=repository:%s:pull"' % repo)
  return loads(o)['token']

def get_docker_image_manifest(repo, tag):
  token = get_docker_token(repo)
  print('Getting image_manifest for %s/%s' % (repo, tag))
  e, o = run_cmd('curl --silent --request "GET" --header "Authorization: Bearer %s" "https://registry-1.docker.io/v2/%s/manifests/%s"' % (token, repo, tag))
  image_manifest=loads(o)
  fsLayers=image_manifest['fsLayers']
  list_of_digests = []
  print('echo fsLayers of %s:%s:' % (repo, tag))
  for a in fsLayers:
    print(a)
  return fsLayers

def has_parent_changed(parent_image, inherited_image, repository):
  parent_image_list = get_docker_image_manifest(*parent_image.split(':'))
  inherited_image_list = get_docker_image_manifest(*inherited_image.split(':'))
  while parent_image_list:
    if inherited_image_list.pop() != parent_image_list.pop():
      return True
  return False

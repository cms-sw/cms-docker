#!/usr/bin/env python

from __future__ import print_function
from json import loads
import sys
import os, glob
from os.path import dirname, abspath
from get_image_config import get_docker_images
import json

if sys.version_info[0] == 2:
  from commands import getstatusoutput as run_cmd
else:
  from subprocess import getstatusoutput as run_cmd

def get_docker_token(repo):
  print('\nGetting docker.io token ....')
  e, o = run_cmd('curl --silent --request "GET" "https://auth.docker.io/token?service=registry.docker.io&scope=repository:%s:pull"' % repo)
  return loads(o)['token']

def get_manifest(image):
  repo = image.split(":",1)[0]
  tag = image.split(":",1)[-1]
  if repo==tag: tag="latest"
  token = get_docker_token(repo)
  print('Getting image_manifest for %s/%s' % (repo, tag))
  e, o = run_cmd('curl --silent --request "GET" --header "Authorization: Bearer %s" "https://registry-1.docker.io/v2/%s/manifests/%s"' % (token, repo, tag))
  return loads(o)

def has_parent_changed(parent, image, repository):
  parent_layers = get_manifest(parent)['fsLayers']
  image_layers = get_manifest(image)['fsLayers']
  while parent_layers and image_layers:
    if parent_layers.pop()!=image_layers.pop():
      return True
  return len(parent_layers)>0


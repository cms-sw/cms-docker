#!/usr/bin/env python
from __future__ import print_function
import yaml
import sys, re
from os.path import exists, join, dirname, abspath

regex_var = re.compile('^(.*)\$\{([^}]+)\}(.*)$')

def push_info(setup, data):
  data.append({})
  for k in setup:
    if k == 'tags': continue
    if type(setup[k])==dict:
      push_info(setup[k], data)
    else:
      data[-1][k]=str(setup[k])

def pop_info(data, cnt):
  while len(data)>cnt: data.pop()
  return

def get_key(key, data):
  for item in data[::-1]:
    if key in item: return item[key]
  return ""

def expand(data):
  nbuilds = []
  for item in data:
    nbuilds.append({})
    for k in item:
      v = item[k]
      while True:
        m = regex_var.match(v)
        if not m: break
        v = "%s%s%s" % (m.group(1), get_key(m.group(2), data), m.group(3))
      nbuilds[-1][k]=v
  return nbuilds

def get_docker_images(name, repository='cmssw'):
  images = []
  setup_file = join(dirname(dirname(abspath(__file__))), name, "config.yaml")
  if not exists(setup_file):
    print("Warnings: No such file %s" % setup_file)
    return images
  setup = yaml.load(open(setup_file))
  data = [{}]
  data[-1]['repository'] = repository
  data[-1]['name'] = name
  data[-1]['contianer'] = join(repository, name)
  push_info(setup, data)
  for image in setup['tags']:
    cnt = len(data)
    for tag in image.keys():
      push_info(image[tag], data)
      data[-1]['tag']=tag
    img_data = expand(data)
    pop_info(data, cnt)

    images.append({})
    images[-1]['BUILD_ARGS']=get_key('args', img_data)
    images[-1]['PUSH']=get_key('push', img_data)
    images[-1]['DOCKER_FILE']=get_key('docker', img_data)
    images[-1]['FROM']=get_key('base', img_data)+":"+get_key('from', img_data)
    images[-1]['CONTAINER']=get_key('repository', img_data)+"/"+get_key('name', img_data)+":"+get_key('tag', img_data)
    images[-1]['TEST_SCRIPT']=get_key('script', img_data)
    images[-1]['TEST_NODE']=get_key('node', img_data)
  return images

#!/usr/bin/env python
from __future__ import print_function
import yaml
import sys, re
from os.path import exists, join, dirname, abspath
from docker_utils import get_manifest
from datetime import datetime
now = datetime.now()

regex_var = re.compile('^(.*?)([$]{1,2})\{([^}]+)\}(.*)$')

def push_info(setup, data, variables=False):
  data.append({})
  for k in setup:
    if k in ['tags', 'groups']: continue
    if type(setup[k])==dict:
      push_info(setup[k], data, variables or k=="variables")
    else:
      sval = str(setup[k])
      if variables:
        if not ".variables" in data[0]:
          data[0][".variables"]={}
        data[0][".variables"][k] = sval
      data[-1][k]=sval

def pop_info(data, cnt):
  while len(data)>cnt: data.pop()
  return

def get_key(key, data):
  for item in data[::-1]:
    if key in item: return item[key]
  return ""

def expand_var(var, data):
  stack = []
  expanded = {}
  while True:
    stack.append(var)
    m = regex_var.match(var)
    if not m: return var
    vx = m.group(3)
    if vx in expanded:
      print("Error: variables %s refers to itself" %  vx)
      print("  ","\n  ".join(stack))
      sys.exit(1)
    expanded[vx] = 1
    if m.group(2)=='$$': vx = eval(m.group(3))
    else: vx = get_key(m.group(3), data)
    vx = vx.replace("%s{%s}" % (m.group(2),m.group(3)), '')
    var = "%s%s%s" % (m.group(1), vx, m.group(4))
  return v

def expand(data):
  nbuilds = []
  for item in data:
    nbuilds.append({})
    for k in item:
      if k=='.variables': continue
      v = item[k]
      k = expand_var(k, data)
      nbuilds[-1][k] = expand_var(v, data)
  return nbuilds

def process_tags(setup, data, images):
  if 'tags' not in setup: return
  for tag in setup['tags']:
    cnt = len(data)
    if setup['tags'][tag]:
      push_info(setup['tags'][tag], data)
    data[-1]['tag']=tag
    img_data = expand(data)
    pop_info(data, cnt)
    image_name = get_key('contianer', img_data) + ":"+get_key('tag', img_data)
    override = get_key('override', img_data).upper()
    if override in ["", "FALSE"]:
      manifest = get_manifest(image_name)
      if 'fsLayers' in manifest: continue
      if not 'errors' in manifest: continue
      if manifest['errors'][0]['code'] != 'MANIFEST_UNKNOWN': continue

    images.append({})
    images[-1]['DOCKER_REPOSITORY']=get_key('repository', img_data)
    images[-1]['DOCKER_NAME']=get_key('name', img_data)
    images[-1]['DOCKER_CONTAINER']=get_key('contianer', img_data)
    images[-1]['IMAGE_NAME']=image_name
    images[-1]['IMAGE_TAG']=get_key('tag', img_data)

    base_image = get_key('from', img_data)
    if not '/' in base_image: base_image="library/"+base_image
    if not ':' in base_image: base_image=base_image+":latest"
    images[-1]['BASE_DOCKER_REPOSITORY']= base_image.split("/")[0]
    images[-1]['BASE_DOCKER_NAME']=base_image.split(":")[0].split("/")[1]
    images[-1]['BASE_DOCKER_CONTAINER']=base_image.split(":")[0]
    images[-1]['BASE_IMAGE_NAME']=base_image
    images[-1]['BASE_IMAGE_TAG']=base_image.split(":")[1]

    images[-1]['IMAGE_BUILD_ARGS']=get_key('args', img_data)
    images[-1]['IMAGE_PUSH']=get_key('push', img_data)
    images[-1]['DOCKER_FILE']=get_key('docker', img_data)
    images[-1]['TEST_SCRIPT']=get_key('script', img_data)
    images[-1]['TEST_NODE']=get_key('node', img_data)
    for xkey in ['delete_pattern', 'expires_days']:
      val = get_key(xkey, img_data)
      if val:
        images[-1][xkey.upper()]=val

    if ".variables" in data[0]:
      for v in data[0][".variables"]:
        images[-1][v] = get_key(v, img_data)
  return
  

def process_groups(setup, data, images):
  if 'groups' not in setup: return
  for group in setup['groups']:
    cnt = len(data)
    push_info(setup['groups'][group], data)
    process_tags(setup['groups'][group], data, images)
    process_groups(setup['groups'][group], data, images)
    pop_info(data, cnt)

def get_docker_images(name, repository='cmssw'):
  images = []
  setup_file = join(dirname(dirname(abspath(__file__))), name, "config.yaml")
  if not exists(setup_file):
    print("Warnings: No such file %s" % setup_file)
    return images
  with open(setup_file) as file:
    setup = yaml.load(file, Loader=yaml.FullLoader)
  data = [{}]
  data[-1]['repository'] = repository
  data[-1]['name'] = name
  data[-1]['contianer'] = join(repository, name)
  push_info(setup, data)
  if not 'groups' in setup:
    setup['groups'] = {'default' : {'tags': dict(setup['tags'])}}
    del setup['tags']
  process_groups(setup, data, images)
  return images

if __name__ == "__main__":
  for name in sys.argv[1:]:
    for img in get_docker_images(name):
      print (img)

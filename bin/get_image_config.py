#!/usr/bin/env python
from __future__ import print_function
import yaml
import sys, re
from os.path import exists, join, dirname, abspath
from docker_utils import get_manifest

regex_var = re.compile('^(.*)\$\{([^}]+)\}(.*)$')

def push_info(setup, data, variables=False):
  data.append({})
  for k in setup:
    if k == 'tags': continue
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

def expand(data):
  nbuilds = []
  for item in data:
    nbuilds.append({})
    for k in item:
      if k=='.variables': continue
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
  for tag in setup['tags']:
    cnt = len(data)
    push_info(setup['tags'][tag], data)
    data[-1]['tag']=tag
    img_data = expand(data)
    pop_info(data, cnt)
    image_name = get_key('contianer', img_data) + ":"+get_key('tag', img_data)
    override = get_key('override', img_data)
    if override in ["", "False"]:
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
    if ".variables" in data[0]:
      for v in data[0][".variables"]:
        images[-1][v] = get_key(v, img_data)
  return images

if __name__ == "__main__":
  for name in sys.argv[1:]:
    for img in get_docker_images(name):
      print (img)

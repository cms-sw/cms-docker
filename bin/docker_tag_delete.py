#!/usr/bin/env python

from __future__ import print_function
from json import loads
from os.path import dirname, abspath
from get_image_config import get_docker_images
from datetime import datetime
from os.path import expanduser
from urllib import request, parse
import sys, re, yaml, os, glob

if sys.version_info[0] == 2:
  from commands import getstatusoutput as run_cmd
else:
  from subprocess import getstatusoutput as run_cmd

def get_registryAPI_token(repo):
  e, o = run_cmd('curl --silent --request "GET" \
"https://auth.docker.io/token?service=registry.docker.io&scope=repository:%s:pull"' % repo)
  return loads(o)['token']

def get_dockerHubToken():
  url = 'https://hub.docker.com/v2/users/login/'
  docker_token = open(expanduser("~/.docker-token")).read().strip()
  data = parse.urlencode(loads(docker_token)).encode()
  req =  request.Request(url, data=data)
  content = request.urlopen(req).read().decode()
  return loads(content)['token']

def logout(token):
  e, o = run_cmd('curl -i -X POST -H "Accept: application/json" -H "Authorization: JWT %s" \
https://hub.docker.com/v2/logout/'%(token))

def deleteTag(dockerHubToken, repo, tag):
  print('Deleting tag: %s....'%tag)
  e, o = run_cmd('curl -s -X DELETE -H "Accept: application/json" -H "Authorization: JWT %s" \
  https://hub.docker.com/v2/repositories/%s/tags/%s/'%(dockerHubToken, repo, tag))
  print(o)

def find_repos():
  repos = []
  dir = os.path.dirname(dirname(os.path.abspath(__file__)))
  for file in glob.glob(dir + '/**/*.yaml*'):
    repos.append(os.path.basename(dirname(file)))
  return(repos)

def get_tags(image):
  repo = image.split(":",1)[0]
  if '/' not in repo:
    repo = 'library/'+repo
  tag = image.split(":",1)[-1]
  if repo==tag:
    tag='latest'
  print('\n========= Tags of %s image: ========='%image)
  token = get_registryAPI_token(repo)
  e, o = run_cmd('curl --silent --request "GET" --header "Authorization: Bearer %s" \
"https://registry-1.docker.io/v2/%s/tags/list?n=500"' % (token, image))
  return(loads(o)['tags'])

def date_diff(regex_pattern, tag):
  timeTag = re.match(regex_pattern, tag)
  if timeTag:
    timeTag = timeTag.group(1)[:8]
    today_date = datetime.now()
    tag_date = datetime.strptime(timeTag, '%Y%m%d')
    return (today_date - tag_date).days
  return 0

dockerHubToken = get_dockerHubToken()
dockerUser = 'cmssw'

for repo in find_repos():
  try:
    tags = get_tags(dockerUser + '/' + repo)
  except KeyError:
    print('Docker Hub user "%s" does not contain image "%s"'%(dockerUser, repo))
    continue
  tagCounter = 0
  for tag in tags:
    tagCounter += 1
    print("{}. {}".format(tagCounter, tag))
    for image in get_docker_images(repo):
      if not image['IMAGE_TAG'] in tag: 
        continue
      if ('DELETE_PATTERN' in image) and ('EXPIRES_DAYS' in image):
        delete_pattern = image['DELETE_PATTERN']
        expires_days = int(image['EXPIRES_DAYS'])
        days = date_diff(delete_pattern, tag)
        if not days: continue
        if days > expires_days:
          deleteTag(dockerHubToken,(dockerUser + '/' + repo), tag)
          break
      else:
        print('Required keys are not provided in config.yaml for "%s" repo.\n\
Nothing to delete.\n'%repo)
logout(dockerHubToken)

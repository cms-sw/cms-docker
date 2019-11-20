#!/usr/bin/env python

from __future__ import print_function
from os.path import dirname, abspath
from get_image_config import get_docker_images
from datetime import datetime
from docker_utils import get_dockerHubToken, get_docker_token, deleteTag, logout, get_tags
import sys, re, yaml, os, glob

def find_repos():
  repos = []
  dir = os.path.dirname(dirname(os.path.abspath(__file__)))
  for file in glob.glob(dir + '/**/*.yaml*'):
    repos.append(os.path.basename(dirname(file)))
  return(repos)

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

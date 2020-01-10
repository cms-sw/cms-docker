#!/usr/bin/env python

from __future__ import print_function
from os.path import dirname, abspath
from get_image_config import get_docker_images
from datetime import datetime
from argparse import ArgumentParser
from docker_utils import get_token, delete_tag, logout, get_tags
import sys, re, yaml, os, glob

def find_repos():
  repos = []
  dir = os.path.dirname(dirname(os.path.abspath(__file__)))
  for file in glob.glob(dir + '/**/*.yaml*'):
    repos.append(os.path.basename(dirname(file)))
  return(repos)

def date_diff(regex_pattern, tag):
  timeTag = re.match('^'+regex_pattern+'$', tag)
  if timeTag:
    timeTag = timeTag.group(1)[:8]
    today_date = datetime.now()
    tag_date = datetime.strptime(timeTag, '%Y%m%d')
    return (today_date - tag_date).days
  return 0

parser = ArgumentParser(description='Delete expired tags from docker repository')
parser.add_argument('-n', '--dry-run', dest='dryRun',     help="List tags which are ready to be removed.", action="store_true", default = False)
parser.add_argument('-u', '--user',    dest='dockerUser', help="Provide Docker Hub username for docker images.", type=str,      default = 'cmssw')
args = parser.parse_args()

for repo in find_repos():
  got_tags = False
  tags = []
  for image in get_docker_images(repo):
    if (not 'DELETE_PATTERN' in image) or (not 'EXPIRES_DAYS' in image):
      continue
    if not got_tags:
      got_tags = True
      try:
        ok, tags = get_tags(args.dockerUser + '/' + repo)
        if not ok:
          tags = []
          print('Docker Hub user "%s" does not contain image "%s"'%(args.dockerUser, repo))
          break
    print("Checking  %s/%s" % (repo, image['IMAGE_TAG']))
    ntags = []
    for tag in tags:
      ntags.append(tag)
      if not tag.startswith(image['IMAGE_TAG']): continue
      delete_pattern = image['DELETE_PATTERN']
      expires_days = int(image['EXPIRES_DAYS'])
      days = date_diff(delete_pattern, tag)
      if not days: continue
      if days > expires_days:
        delete_tag((args.dockerUser + '/' + repo), tag, args.dryRun)
        ntags.remove(tag)
    tags = ntags[:]

logout()

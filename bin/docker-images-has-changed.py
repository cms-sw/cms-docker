#!/usr/bin/env python
from argparse import ArgumentParser
from get_image_config import get_docker_images
from docker_utils import has_parent_changed
import glob, os
from os.path import dirname
import json

def create_file(img):
  print('Writing to file ....')
  file_name = (img.get('CONTAINER').replace('/', '_').replace(':', '_') + '.txt')
  with open(file_name,'w+') as file:
    for key, value in img.items():
      line = str(key) + '=' + str(value) + '\n'
      file.write(line)
  file.close()
  print('{} file created'.format(file_name))

parser = ArgumentParser(description='Check if docker image based on the same layers as the parent image')
parser.add_argument('-r', dest='repo', type=str, help="Provide specific repository for docker images.")
args = parser.parse_args()
if args.repo:
  images_to_compare(args.repo)
else:
  dir = os.path.dirname(dirname(os.path.abspath(__file__)))
  for file in glob.glob(dir + '/**/*.yaml*'):
    reponame = os.path.basename(dirname(file)) # gets name of folder where .yaml file founded
    for img in get_docker_images(reponame):
      inher= img.get('CONTAINER')
      parent = img.get('FROM')
      if has_parent_changed(parent, inher, reponame):
         create_file(img)

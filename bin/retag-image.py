#!/usr/bin/env python
from __future__ import print_function
from argparse import ArgumentParser
from docker_utils import get_digest_of_image

parser = ArgumentParser(description='')
parser.add_argument('-r', dest='repository',  type=str, help="Docker container repository e.g. cmssw/cms")
parser.add_argument('-s', dest='source',      type=str, help="Existing docker image tag e.g rhel6-itb")
parser.add_argument('-d', dest='destination', type=str, help="New docker image tag e.g rhel6")
args = parser.parse_args()
if not (args.repository and args.source and args.destination):
  parser.error("Missing arguments.")

src = get_digest_of_image(args.repository, args.source)
if not src[0]:
  print("ERROR: Unable to find source image %s:%s" % (args.repository, args.source))
  sys.exit(1)

des = get_digest_of_image(args.repository, args.destination)
print("%s vs %s" % (src[1], des[1]))
if src[1] != des[1]:
  print("SOURCE_IMAGE=%s:%s" % (args.repository, args.source))
  print("DESTINATION_IMAGE=%s:%s" % (args.repository, args.destination)) 

#!/usr/bin/env python3
import sys, re
from argparse import ArgumentParser
from os.path import join,dirname,abspath
from get_image_config import get_docker_images

def prepare_Dockerfile(img, outfile):
  reg = re.compile("^([^@]*)@([^@]+)@(.*)")
  docfile = join(dirname(dirname(abspath(__file__))), img['DOCKER_NAME'], img['DOCKER_FILE'])
  out = []
  with open(docfile) as ref:
    for line in [l.strip() for l in ref.readlines()]:
      while True:
        m = reg.match(line)
        if m:
          val = ""
          if m.group(2) in img: val = img[m.group(2)]
          line = "%s%s%s" % (m.group(1), val, m.group(3))
        else:
          break
      out.append("%s\n" % line)
  with open(outfile, "w") as ref:
    for l in out:
      ref.write(l)
  print("Dockerfile prepared:",outfile)
  return

parser = ArgumentParser(description='Prepare dockerfile')
parser.add_argument('-c', dest='container', type=str, help="Docker container full name e.g. cmssw/el9:x86_64-grid")
parser.add_argument("-o", "--out-file", dest="outFile", type=str, help="Name of the newly created DockerFile", default="Dockerfile.new")

args = parser.parse_args()
if not args.container:
  parser.print_help()
  sys.exit(1)

m = re.match("^cmssw/([a-z0-9]+):.+$", args.container)
if not m:
  print("Error: Invalid image name: %s" % args.container)
  parser.print_help()
  sys.exit(1)

data = get_docker_images(m.group(1))
for img in data:
  if img['IMAGE_NAME'] != args.container:
    print("Skipping container",img['IMAGE_NAME'])
    continue
  prepare_Dockerfile(img, args.outFile)
  break


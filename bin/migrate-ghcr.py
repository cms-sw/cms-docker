#!/usr/bin/env python3
import sys, yaml
from subprocess import getstatusoutput as run_cmd
from os.path import join, dirname, abspath
from docker_utils import get_tags, get_repos, hub_request
from time import sleep
import threading
topdir = dirname(dirname(abspath(__file__)))
sys.path.insert(0,join(topdir,'..', "cms-bot"))
from github_utils import get_org_packages, get_org_package_versions, get_org_package_version

token_file = "/afs/cern.ch/user/m/muzaffar/.gh_container"

def get_manifest(image):
  e , sha = run_cmd("docker manifest inspect %s | grep '\"digest\"' | head -1 | sed 's|.*sha256:||;s|\".*||'" % image)
  return sha.strip()

def create_repo (name, repo):
  print("  Creating ",name, repo)
  e, o = run_cmd("%s/bin/create-gh-package.sh %s %s" % (topdir, name, repo))
  if e:
    print(o)
    return False
  return True

def push_tag(name, tag):
  print("  Pushing tag cmssw/%s:%s" % (name, tag))
  e, o = run_cmd("%s/bin/hub2ghcr.sh %s %s" % (topdir, name, tag))
  if e:
    print(o)
    return False
  return True

def add_tags(name):
  rname = "cmssw%%2F%s" % name
  res, hub_tags = get_tags(rname, full=True)
  if not res: return res
  gh_tags = get_org_package_versions("cms-sw", package=rname, token_file=token_file)
  gh_sha = {}
  hub_sha = {}
  for tag in gh_tags:
    for v in tag['metadata']['container']['tags']:
      gh_sha[v] = tag['name']
  moving_tags = [ "latest", "x86_64", "aarch64", "ppc64le", "x86_64-bootstrap", "aarch64-bootstrap", "ppc64le-bootstrap"]
  for tag in hub_tags:
    try:
      sha=tag['digest']
    except:
      try:
        sha = tag['images'][-1]['digest']
      except:
        print("  ERROR: No digest",tag['name'],tag)
        continue
    tag_name = tag['name']
    if (not tag_name in moving_tags) and (tag_name in gh_sha):
      print("  Tag exists:",tag_name)
      continue
    if not tag_name.startswith("tmp-"):
      hub_sha[tag_name] = sha
  jobs = []
  max_jobs = 1
  for tag_name in hub_sha:
    if (tag_name in gh_sha) and (hub_sha[tag_name]==gh_sha[tag_name]):
      print("  Tag exists:",tag_name)
      continue
    img = "cmssw/%s:%s" % (name, tag_name)
    if get_manifest(img) == get_manifest("ghcr.io/cms-sw/"+img):
      print("  Tag exists:",tag_name)
    else:
      while (len(jobs) >= max_jobs):
        sleep(0.1)
        ajobs = []
        for t in jobs:
          if t.is_alive(): ajobs.append(t)
        jobs = ajobs[:]
      t = threading.Thread(target=push_tag, args=(name, tag_name))
      t.start()
      jobs.append(t)
      sleep(0.1)
  for t in jobs: t.join()
  return True

name_repo_map = {
  'cmssw' : 'cms-docker',
  'dmwm'  : 'dmwm-containers',
}

repo_conf_file = join(topdir, "docker-config.yaml")
repo_conf = {}
with open(join(dirname(dirname(abspath(__file__))), "docker-config.yaml")) as ref:
  try:
    from yaml import FullLoader
    repo_conf = yaml.load(ref, Loader=FullLoader)
  except ImportError as e:
    repo_conf = yaml.load(ref)

gh_repos = get_org_packages("cms-sw", token_file=token_file)
for name in repo_conf['repositories']:
  #if name!="ubi8": continue
  fname = "cmssw/%s" % name
  repo_obj = repo_conf['repositories'][name]
  found=False
  print("Working on ",fname)
  for team in name_repo_map:
    if team in repo_obj:
      if not [True for r in gh_repos if r['name']==fname]:
        create_repo (name, name_repo_map[team])
      else:
        print("  OK already exists.")
      if not add_tags(name):
        sys.exit(1)
      found=True
      break
  if not found:
    print("ERROR: Unknown team: ",team,repo_obj)

#!/usr/bin/env python3
import sys, yaml
from subprocess import getstatusoutput as run_cmd
from os.path import join, dirname, abspath
from docker_utils import get_tags, get_repos, hub_request
topdir = dirname(dirname(abspath(__file__)))
sys.path.insert(0,join(topdir,'..', "cms-bot"))
from github_utils import get_org_packages, get_org_package_versions

token_file = "/afs/cern.ch/user/m/muzaffar/.gh_container"

def create_repo (name, repo):
  print("Creating ",name, repo)
  e, o = run_cmd("%s/bin/create-gh-package.sh %s %s" % (topdir, name, repo))
  if e:
    print(o)
    return False
  return True

def add_tags(name):
  rname = "cmssw%%2F%s" % name
  res, hub_tags = get_tags(rname, full=True)
  if not res: return res
  print("Getting tags for ", rname)
  gh_tags = get_org_package_versions("cms-sw", package=rname, token_file=token_file)
  print("========== gh")
  for tag in gh_tags: print(tag)
  print("======= doc")
  for tag in hub_tags: print(tag)
  return False

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
  if name!="el8": continue
  fname = "cmssw/%s" % name
  repo_obj = repo_conf['repositories'][name]
  found=False
  for team in name_repo_map:
    if team in repo_obj:
      if not [True for r in gh_repos if r['name']==fname]:
        create_repo (name, name_repo_map[team])
      if not add_tags(name):
        sys.exit(1)
      found=True
      break
  if not found:
    print("ERROR: Unknown team: ",team,repo_obj)

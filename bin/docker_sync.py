#!/usr/bin/env python

from __future__ import print_function
from docker_utils import (get_repos, get_teams, get_permissions, get_members, logout, create_repo, create_team, 
                          add_permissions, add_member, delete_repo, delete_team, delete_permissions, delete_member)
from argparse import ArgumentParser
import yaml
import sys
from os.path import join, dirname, abspath

parser = ArgumentParser(description='Synchronize Docker HUB with yaml configuration file')
parser.add_argument('-u', '--username', dest='username', help="Provide Docker Hub username for synchronization", type=str, default='org0namespace')
parser.add_argument('-n', '--disable', dest='dryrun', help="Dry Run mode enabled by default. Disable it to make changes to docker hub", action="store_false", default=True)
args = parser.parse_args()
if not args.dryrun:
  print('==== DRY RUN MODE DISABLED ====')
yaml_location = join(dirname(dirname(abspath(__file__))), "docker_config.yaml")
with open(yaml_location) as file:
  yaml_file = yaml.load(file, Loader=yaml.FullLoader)

def update_dockerhub(config_file, docker_hub, username = args.username, team_name = None, repo = None, 
                     team_id = None, yaml_permissions = None, what_to_sync = None, dryrun=args.dryrun):
  dryrun_message = 'Dry run mode enabled, no changes to Docker Hub applied'
  diff_list = [item for item in config_file + docker_hub if item not in config_file or item not in docker_hub]
  for list_item in diff_list:
    if list_item in config_file and list_item not in docker_hub:
      if what_to_sync == 'repos':
        print('Adding repository: "%s"' % list_item)
        print(dryrun_message) if dryrun else print(create_repo(username, list_item)[0])
      elif what_to_sync == 'teams':
        print('Creating team: "%s"' % list_item)
        print(dryrun_message) if dryrun else print(create_team(username, list_item)[0])
      elif what_to_sync == 'permissions':
        print('Adding "%s" permission to "%s" repository for "%s" team:' % (yaml_permissions[list_item], list_item, team_name))
        print(dryrun_message) if dryrun else print(add_permissions(username, list_item, team_id, yaml_permissions[list_item])[0])
      elif what_to_sync == 'members':
        print('Adding member "%s" to "%s" team:' % (list_item, team_name))
        print(dryrun_message) if dryrun else print(add_member(username, team_name, list_item)[0])
    if list_item in docker_hub and list_item not in config_file:
      if what_to_sync == 'repos':
        print('Deleting repository: "%s"' % list_item)
        print(dryrun_message) if dryrun else print(delete_repo(username, list_item)[0])
      elif what_to_sync == 'teams':
        print('Deleting team: "%s"' % list_item)
        print(dryrun_message) if dryrun else print(delete_team(username, list_item)[0])
      elif what_to_sync == 'permissions':
        print('Deleting permission for "%s" repository from "%s" team:' % (list_item, team_name))
        print(dryrun_message) if dryrun else print(delete_permissions(username, list_item, team_id)[0])
      elif what_to_sync == 'members':
        print('Deleting member "%s" from "%s" team:' % (list_item, team_name))
        print(dryrun_message) if dryrun else print(delete_member(username, team_name, list_item)[0])

# UPDATE REPOSITORIES:
print('\n----- Synchronizing repositories for "%s":' % args.username)
hub_repos = get_repos(args.username)
print(hub_repos)
print(yaml_file['repositories'])
if not hub_repos[0]: print(hub_repos[1]) & sys.exit(1)
if hub_repos[1] == []:
  print('No repositories found. Check Docker Hub username')
  sys.exit(1)
update_dockerhub(yaml_file['repositories'], hub_repos[1], what_to_sync='repos')
# UPDATE TEAMS:
print('\n----- Synchronizing teams for "%s":' % args.username)
hub_teams = get_teams(args.username)
print(hub_teams)
print(yaml_file['teams'].keys())
if not hub_teams[0]: print(hub_teams[1]) & sys.exit(1)
update_dockerhub(list(yaml_file['teams'].keys()), list(hub_teams[1].keys()), what_to_sync='teams')
for team_name in hub_teams[1]:
  team_id = hub_teams[1][team_name]
  if team_name != 'owners':
  # UPDATE PERMISSIONS:
    print('\n----- Synchronizing permissions for "%s" team:' % team_name)
    hub_permissions = get_permissions(args.username, team_name)
    print(hub_permissions)
    if not hub_permissions[0]: print(hub_permissions[1]) & sys.exit(1)
    yaml_permissions = yaml_file['teams'][team_name]['permissions']
    print(yaml_permissions)
    if yaml_permissions is None:
      print('No repository permissions found in yaml config file for "%s"' % team_name)
      yaml_repo_access = []
    else:
      yaml_repo_access = yaml_permissions.keys()
    docker_repo_access = []
    docker_repo_access = hub_permissions[1].keys()
    update_dockerhub(yaml_repo_access, docker_repo_access, team_name=team_name, 
    team_id=team_id, yaml_permissions=yaml_permissions, what_to_sync = 'permissions')
    # UPDATE MEMBERS:
    print('\n----- Synchronizing members for "%s":' % team_name)
    hub_team_members = get_members(args.username, team_name)
    print(hub_team_members)
    if not hub_team_members[0]: print(hub_team_members[1]) & sys.exit(1)
    members_in_yaml = yaml_file['teams'][team_name]['members']
    print(members_in_yaml)
    if members_in_yaml is None: members_in_yaml = []
    update_dockerhub(members_in_yaml, hub_team_members[1], team_name=team_name, what_to_sync='members')
logout()
#!/usr/bin/env python

from __future__ import print_function
from docker_utils import (get_repos, get_teams, get_permissions, get_members, logout, create_repo, create_team, 
                          add_permissions, add_member, delete_repo, delete_team, delete_permissions, delete_member)
from argparse import ArgumentParser
import yaml

parser = ArgumentParser(description='Synchronize Docker HUB with yaml configuration file')
parser.add_argument('-u', '--username', dest='username', help="Provide Docker Hub username for synchronization", type=str, default='cmssw')
parser.add_argument('-n', '--disable', dest='dryrun', help="Dry Run mode enabled by default. Disable it to make changes to docker hub", action="store_false", default=True)
args = parser.parse_args()
print('==============',args.dryrun)
with open('docker_config.yaml') as file:
  data = yaml.load(file, Loader=yaml.FullLoader)

def update_dockerhub(config_file, docker_hub, username = args.username, team_name = None, repo = None, 
                     team_id = None, yaml_permissions = None, what_to_sync = None, dryrun=args.dryrun):
  diff_list = [item for item in config_file + docker_hub if item not in config_file or item not in docker_hub]
  for list_item in diff_list:
    if list_item in config_file and list_item not in docker_hub:
      if what_to_sync == 'repos':
        print('Adding repository: "%s"' % list_item)
        print(create_repo(username, list_item, dryrun))
      elif what_to_sync == 'teams':
        print('Creating team: "%s"' % list_item)
        print(create_team(username, list_item, dryrun))
      elif what_to_sync == 'permissions':
        print('Adding "%s" permission to "%s" repository for "%s" team:' % (yaml_permissions[list_item], list_item, team_name))
        print(add_permissions(username, list_item, team_id, yaml_permissions[list_item], dryrun))
      elif what_to_sync == 'members':
        print('Adding member "%s" to "%s" team:' % (list_item, team_name))
        member_is_added =  add_member(username, team_name, list_item, dryrun)
        print(member_is_added[3]) if not member_is_added[0] else print(member_is_added)

    if list_item in docker_hub and list_item not in config_file:
      if what_to_sync == 'repos':
        print('Deleting repository: "%s"' % list_item)
        print(delete_repo(username, list_item, dryrun))
      elif what_to_sync == 'teams':
        print('Deleting team: "%s"' % list_item)
        print(delete_team(username, list_item, dryrun))
      elif what_to_sync == 'permissions':
        print('Deleting permission for "%s" repository from "%s" team:' % (list_item, team_name))
        print(delete_permissions(username, list_item, team_id, dryrun))
      elif what_to_sync == 'members':
        print('Deleting member "%s" from "%s" team:' % (list_item, team_name))
        print(delete_member(username, team_name, list_item, dryrun))

#UPDATE REPOSITORIES:
print('\n----- Synchronizing repositories for "%s":' % args.username)
update_dockerhub(data['repositories'], get_repos(args.username), what_to_sync='repos')
# UPDATE TEAMS:
print('\n----- Synchronizing teams for "%s":' % args.username)
update_dockerhub(list(data['teams'].keys()), list(get_teams(args.username).keys()), what_to_sync='teams')
for team_name in get_teams(args.username):
  team_id = get_teams(args.username)[team_name]
  if team_name != 'owners':
  # UPDATE PERMISSIONS:
    print('\n----- Synchronizing permissions for "%s" team:' % team_name)
    yaml_permissions = data['teams'][team_name]['permissions']
    if yaml_permissions is None:
      print('No repository permissions found in yaml config file for "%s"' % team_name)
      yaml_repo_access = []
    else:
      yaml_repo_access = yaml_permissions.keys()
    hub_repo_access = []
    for item in get_permissions(args.username, team_name):
      hub_repo_access.append(item['repository'])
    update_dockerhub(yaml_repo_access, hub_repo_access, team_name=team_name, 
    team_id=team_id, yaml_permissions=yaml_permissions, what_to_sync = 'permissions')
    # UPDATE MEMBERS:
    print('\n----- Synchronizing members for "%s":' % team_name)
    members_in_yaml = data['teams'][team_name]['members']
    if members_in_yaml is None: members_in_yaml = []
    update_dockerhub(members_in_yaml, get_members(args.username, team_name), team_name=team_name, what_to_sync='members')
logout()
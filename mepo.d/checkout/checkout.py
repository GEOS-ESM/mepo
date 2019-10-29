import os
import sys
import csv
import json
import subprocess as sp

from mepo_state import MepoState

def run(args):
    MepoState.initialize(args.cf)
    allrepos = MepoState.read_state()
    print 'Checking out components...'
    for name, repo in allrepos.items():
        __checkout_component(name, repo)

def __checkout_component(name, repo):
    version, identifier = __get_version(repo)
    __git_clone(repo['remote'], version, repo['local'])
    print('{:<{width}} ({:<1s}) {:<s}'.
          format(name, identifier, version, width=30))

def __get_version(repo):
    if 'tag' not in repo and 'branch' not in repo:
        raise Exception('Need to specify one of [tag, branch]')
    if 'tag' in repo and 'branch' in repo:
        raise Exception('Can specify only one of [tag, branch], not both')
    identifier = 't'
    version = repo.get('tag')
    if version is None:
        identifier = 'b'
        version = repo.get('branch')
    return (version, identifier)

def __git_clone(url, version, local_path):
    cmd = 'git clone -b %s %s %s' % (version, url, local_path)
    output_file = os.path.join(MepoState.get_dir(), 'checkout.log')
    with open(output_file, 'a') as fnull:
        sp.check_call(cmd.split(), stderr=fnull)

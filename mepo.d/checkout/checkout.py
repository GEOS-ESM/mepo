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
    for reponame in allrepos:
        __checkout_components(reponame, allrepos[reponame])

def __get_version(branch_name, tag_name):
    if not branch_name and not tag_name:
        raise Exception('Need to specify one of [tag, branch]')
    if branch_name and tag_name:
        raise Exception('Can specify only one of [tag, branch], not both')
    if branch_name:
        return (branch_name, 'b')
    elif tag_name:
        return (tag_name, 't')

def __checkout_components(name, repo):
    version, identifier = __get_version(repo['branch'], repo['tag'])
    __git_clone(repo['origin'], version, repo['path'])
    print('{:<{width}} ({:<1s}) {:<s}'.
          format(name, identifier, version, width=30))

def __git_clone(url, version, local_path):
    cmd = 'git clone -b %s %s %s' % (version, url, local_path)
    output_file = os.path.join(MepoState.get_dir(), 'checkout.log')
    with open(output_file, 'a') as fnull:
        sp.check_call(cmd.split(), stderr=fnull)

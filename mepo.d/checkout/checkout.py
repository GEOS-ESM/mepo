import os
import sys
import csv
import json
import subprocess as sp

from Mepo import MepoState

def run(args):
    MepoState.initialize(args.cf)
    allrepos = MepoState.read_state()
    print 'Checking out components...'    
    for repo in allrepos:
        __checkout_components(repo)

def __get_branch_or_tag(branch_name, tag_name):
    if not branch_name and not tag_name:
        raise Exception('Need to specify one of [tag, branch]')
    if branch_name and tag_name:
        raise Exception('Can specify only one of [tag, branch], not both')
    if branch_name:
        return (branch_name, 'b')
    elif tag_name:
        return (tag_name, 't')
    
def __checkout_components(repo):
    branch_or_tag, identifier = __get_branch_or_tag(repo['branch'], repo['tag'])
    __git_clone(repo['origin'], branch_or_tag, repo['path'])
    print('     {:<30s} {:<3s}{:<40s}'.format(repo['name'][:30], identifier, branch_or_tag[:40]))
    
def __git_clone(url, branch_or_tag, local_path):
    cmd = 'git clone -b %s %s %s' % (branch_or_tag, url, local_path)
    output_file = os.path.join(MepoState.mepo_state_dir, 'checkout.log')
    with open(output_file, 'a') as fnull:
        sp.check_call(cmd.split(), stderr=fnull)

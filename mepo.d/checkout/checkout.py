import os
import sys
import csv
import json
import subprocess as sp

from mepo_state import MepoState

def run(args):
    allrepos = MepoState.initialize(args.cf)
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        version, vtype = get_version(repo)
        checkout_component(name, repo, version)
        print_status(name, version, vtype, max_name_length)

def checkout_component(name, repo, version):
    git_clone(repo['remote'], version, repo['local'])

def get_version(repo):
    vtype = 't'
    version = repo.get('tag')
    if version is None:
        vtype = 'b'
        version = repo.get('branch')
    return (version, vtype)

def git_clone(url, version, local_path):
    cmd = 'git clone -b %s %s %s' % (version, url, local_path)
    output_file = os.path.join(MepoState.get_dir(), 'checkout.log')
    with open(output_file, 'a') as fnull:
        sp.check_call(cmd.split(), stderr=fnull)

def print_status(name, version, vtype, width):
    FMT = '{:<{width}} | {:<1.1s} | {:<s}'
    print(FMT.format(name, vtype, version, width = width))

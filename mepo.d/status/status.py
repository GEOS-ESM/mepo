import os
import sys
import json
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        version, vtype = get_current_version(name, repo)
        relpath = get_relative_path(repo)
        output = check_status(name, repo)
        print_status(name, relpath, version, vtype, output, max_name_length)

def check_status(name, repo, verbose=False):
    cmd = 'git -C %s status -s' % repo['local']
    output = sp.check_output(cmd.split())
    return output

def get_relative_path(repo):
    return os.path.relpath(repo['local'], os.getcwd())

def get_current_version(name, repo):
    repo_path = repo['local']
    version, vtype = get_repo_branch_name(repo_path)
    if version is None:
        version, vtype = get_repo_tag_name(repo_path)
        if version is None:
            sys.exit('Could not find branch or tag name for %s' % name)
    return (version.strip(), vtype)

def get_repo_branch_name(repo_path):
    cmd = 'git -C %s symbolic-ref -q --short HEAD' % repo_path
    try:
        with open(os.devnull, 'w') as ferr:
            version = sp.check_output(cmd.split(), stderr = ferr)
        return (version, 'b')
    except sp.CalledProcessError:
        return (None, None)

def get_repo_tag_name(repo_path):
    cmd = 'git -C %s describe --tags --exact-match' % repo_path
    try:
        with open(os.devnull, 'w') as ferr:
            version = sp.check_output(cmd.split(), stderr = ferr)
        return (version, 't')
    except sp.CalledProcessError:
        return (None, None)

def print_status(name, relpath, version, vtype, output, width):
    PATH_LEN = 50
    FMT_FULL = '{:<%s.%ss} | {:<%ss} | ({:<1.1s}) {:<s}' % (width, width, PATH_LEN)
    FMT1 = '{:<%s.%ss} | {:<s}' % (width, width)
    FMT2 = '{:^%s.%ss}   {:>%ss} | ({:<1.1s}) {:<s}' % (width, width, PATH_LEN)
    if len(relpath) > PATH_LEN:
        print(FMT1.format(name, relpath + ' ...'))
        print(FMT2.format('', '...', vtype, version))
    else:
        print(FMT_FULL.format(name, relpath, vtype, version))
    if (output):
        for line in output.strip().split('\n'):
            print '   |', line.rstrip()

import os
import sys
import subprocess as sp

from Mepo import MepoState

def run(branch_name):
    allrepos = MepoState.read_state()
    for repo in allrepos:
        __create_branch(repo, branch_name)

def __create_branch(repo, branch_name):
    cwd = os.getcwd()
    os.chdir(repo['path'])
    print repo['name'],
    cmd = 'git checkout -b %s' % branch_name
    sp.check_output(cmd.split())
    os.chdir(cwd)

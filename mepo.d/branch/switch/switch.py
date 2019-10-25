import os
import sys
import subprocess as sp

from Mepo import MepoState

def run(repo_name, branch_name):
    allrepos = MepoState.read_state()
    for repo in allrepos:
        if repo['name'] == repo_name:
            __switch_branch(repo, branch_name)

def __switch_branch(repo, branch_name):
    cwd = os.getcwd()
    os.chdir(repo['path'])
    cmd = 'git checkout -b %s' % branch_name
    try:
        sp.check_output(cmd.split(), stderr = sp.STDOUT)
    except sp.CalledProcessError as err:
        os.chdir(cwd)
        MepoState.error(err.output.strip())

import os
import sys
import subprocess as sp

from mepo_state import MepoState

def run(repo_names, branch_name):
    allrepos = MepoState.read_state()
    for reponame in repo_names:
        if reponame not in allrepos:
            sys.exit('ERROR: invalid repo name [%s]' % reponame)
        create_branch(reponame, allrepos[reponame], branch_name)

def create_branch(reponame, repo, branch_name):
    cwd = os.getcwd()
    os.chdir(repo['local'])
    print reponame+':',
    sys.stdout.flush()
    cmd = 'git checkout -b %s' % branch_name
    sp.check_output(cmd.split())
    os.chdir(cwd)

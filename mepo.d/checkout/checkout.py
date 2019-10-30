import os
import sys
import subprocess as sp

from state.state import MepoState

def run(args):
    repo_name = args.repo_name
    branch_name = args.branch_name
    allrepos = MepoState.read_state()
    for reponame in repo_name:
        if reponame not in allrepos:
            sys.exit('ERROR: invalid repo name [%s]' % reponame)
        __checkout_branch(reponame, allrepos[reponame], branch_name)

def __checkout_branch(name, repo, branch):
    cwd = os.getcwd()
    os.chdir(repo['local'])
    cmd = 'git checkout %s' % branch
    try:
        with open(os.devnull, 'w') as ferr:
            sp.check_output(cmd.split(), stderr = sp.STDOUT)
        os.chdir(cwd)
    except sp.CalledProcessError as err:
        print err.output.strip()
        sys.exit(err.returncode)

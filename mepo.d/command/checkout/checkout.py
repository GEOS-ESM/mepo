import os
import subprocess as sp

from state.state import MepoState

def run(args):
    repo_name = args.repo_name
    branch_name = args.branch_name
    allrepos = MepoState.read_state()
    for reponame in repo_name:
        if reponame not in allrepos:
            raise Exception('invlaid repo name [%s]' % reponame)
        __checkout_branch(reponame, allrepos[reponame], branch_name)

def __checkout_branch(name, repo, branch):
    cmd = 'git -C %s checkout %s' % (repo['local'], branch)
    try:
        with open(os.devnull, 'w') as ferr:
            sp.check_output(cmd.split(), stderr = sp.STDOUT)
    except sp.CalledProcessError as err:
        raise Exception(err.output.strip())

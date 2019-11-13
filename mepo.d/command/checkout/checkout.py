import os
import subprocess as sp

from state.state import MepoState

def run(args):
    repo_name = args.repo_name
    create = args.b
    branch_name = args.branch_name
    allrepos = MepoState.read_state()
    for reponame in repo_name:
        if reponame not in allrepos:
            raise Exception('invlaid repo name [%s]' % reponame)
        if create:
            _create_branch(reponame, allrepos[reponame], branch_name)
        _checkout_branch(reponame, allrepos[reponame], branch_name)

def _checkout_branch(name, repo, branch):
    cmd = 'git -C %s checkout %s' % (repo['local'], branch)
    try:
        with open(os.devnull, 'w') as ferr:
            sp.check_output(cmd.split(), stderr = sp.STDOUT)
    except sp.CalledProcessError as err:
        raise Exception(err.output.strip())

def _create_branch(reponame, repo, branch):
    cmd = 'git -C %s branch %s' % (repo['local'], branch)
    sp.check_output(cmd.split())
    print '+ %s: %s' % (reponame, branch)

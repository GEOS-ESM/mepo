import os

from state.state import MepoState
from utilities import shellcmd

def run(args):
    repo_name = args.repo_name
    create = args.b
    branch_name = args.branch_name
    allrepos = MepoState.read_state()
    for reponame in repo_name:
        if reponame not in allrepos:
            raise Exception('invalid repo name [%s]' % reponame)
        if create:
            _create_branch(reponame, allrepos[reponame], branch_name)
        _checkout_branch(reponame, allrepos[reponame], branch_name)

def _checkout_branch(name, repo, branch):
    cmd = 'git -C %s checkout %s' % (repo['local'], branch)
    shellcmd.run(cmd.split(), output=True).strip()

def _create_branch(reponame, repo, branch):
    cmd = 'git -C %s branch %s' % (repo['local'], branch)
    shellcmd.run(cmd.split())
    print('+ {}: {}'.format(reponame, branch))

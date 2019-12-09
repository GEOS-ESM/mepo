from state.state import MepoState
from utilities import verify
from utilities import shellcmd

def run(args):
    allrepos = MepoState.read_state()
    verify.valid_repos(args.repo_name, allrepos.keys())
    repos_dev = {name: allrepos[name] for name in args.repo_name}
    for name, repo in repos_dev.items():
        if 'develop' not in repo:
            raise Exception("'develop' branch not specified for {}".format(name))
        local_path = repo['local']
        _checkout_branch(local_path, repo['develop'])
        _sync_branch_with_remote(local_path)

def _checkout_branch(local_path, branch):
    cmd = 'git -C {} checkout {}'.format(local_path, branch)
    shellcmd.run(cmd.split())

def _sync_branch_with_remote(local_path):
    cmd = 'git -C {} pull'.format(local_path)
    shellcmd.run(cmd.split())

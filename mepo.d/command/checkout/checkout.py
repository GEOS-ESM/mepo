from state.state import MepoState
from utilities import shellcmd
from utilities import verify

def run(args):
    allrepos = MepoState.read_state()
    verify.valid_repos(args.repo_name, allrepos.keys())
    repos_co = {name: allrepos[name] for name in args.repo_name}
    for name, repo in repos_co.items():
        local_path = repo['local']
        branch_name = args.branch_name
        if args.b:
            _create_branch(local_path, branch_name)
            print('+ {}: {}'.format(name, branch_name))
        _checkout_branch(local_path, branch_name)

def _checkout_branch(local_path, branch):
    cmd = 'git -C {} checkout {}'.format(local_path, branch)
    shellcmd.run(cmd.split())

def _create_branch(local_path, branch):
    cmd = 'git -C {} branch {}'.format(local_path, branch)
    shellcmd.run(cmd.split())

from create import create
from switch import switch

from state.state import MepoState

def run(args):
    branch_cmd = args.mepo_branch_cmd
    branch_name = args.branch_name
    repo_names = args.repo_name
    if branch_cmd == 'create':
        create.run(repo_names, branch_name)
    else:
        raise NotImplementedError('"mepo branch %s" has not yet been implemented' % branch_cmd)

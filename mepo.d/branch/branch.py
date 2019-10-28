from mepo_state import MepoState
from create import create
from switch import switch

def run(args):
    branch_cmd = args.mepo_branch_cmd
    branch_name = args.branch_name
    raise NotImplementedError('"mepo branch %s" has not yet been implemented' % branch_cmd)
    # if branch_cmd == 'create':
    #     create.run(branch_name)
    # elif branch_cmd == 'switch':
    #     switch.run(args.repo_name, args.branch_name)
    # else:
    #     raise NotImplementedError('"mepo branch %s" has not yet been implemented' % branch_cmd)

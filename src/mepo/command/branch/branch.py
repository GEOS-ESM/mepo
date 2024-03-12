import subprocess as sp

from state.state import MepoState

from command.branch.list   import list
from command.branch.create import create
from command.branch.delete import delete

def run(args):
    d = {
        'list': list,
        'create': create,
        'delete': delete,
    }
    d[args.mepo_branch_cmd].run(args)

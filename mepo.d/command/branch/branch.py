import subprocess as sp

from state.state import MepoState

from command.branch.brlist import brlist
from command.branch.create import create
from command.branch.delete import delete

def run(args):
    d = {
        'list': brlist,
        'create': create,
        'delete': delete,
    }
    d[args.mepo_branch_cmd].run(args)

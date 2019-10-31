import subprocess as sp

from state.state import MepoState

from brlist import brlist
from create import create
from delete import delete

def run(args):
    d = {
        'list': brlist,
        'create': create,
        'delete': delete,
    }
    d[args.mepo_branch_cmd].run(args)

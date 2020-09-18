import subprocess as sp

from state.state import MepoState

from command.tag.tglist import tglist
from command.tag.create import create
from command.tag.delete import delete

def run(args):
    d = {
        'list': tglist,
        'create': create,
        'delete': delete
    }
    d[args.mepo_tag_cmd].run(args)

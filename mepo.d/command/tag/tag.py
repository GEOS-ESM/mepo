import subprocess as sp

from state.state import MepoState

from command.tag.list   import list
from command.tag.create import create
from command.tag.delete import delete
from command.tag.push   import push

def run(args):
    d = {
        'list': list,
        'create': create,
        'delete': delete,
        'push': push
    }
    d[args.mepo_tag_cmd].run(args)

import subprocess as sp

from state.state import MepoState

from command.stash.list  import list
from command.stash.pop   import pop
from command.stash.apply import apply
from command.stash.push  import push
from command.stash.show  import show

def run(args):
    d = {
        'list':  list,
        'pop':   pop,
        'apply': apply,
        'push':  push,
        'show':  show,
    }
    d[args.mepo_stash_cmd].run(args)

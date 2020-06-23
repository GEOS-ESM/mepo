import subprocess as sp

from state.state import MepoState

from command.stash.stlist  import stlist
from command.stash.stpop   import stpop
from command.stash.stapply import stapply

def run(args):
    d = {
        'list':  stlist,
        'pop':   stpop,
        'apply': stapply,
    }
    print(args.mepo_stash_cmd)
    d[args.mepo_stash_cmd].run(args)

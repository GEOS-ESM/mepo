import subprocess as sp

from state.state import MepoState

from command.stash.stlist  import stlist
from command.stash.stpop   import stpop
from command.stash.stapply import stapply
from command.stash.stpush  import stpush

def run(args):
    d = {
        'list':  stlist,
        'pop':   stpop,
        'apply': stapply,
        'push':  stpush,
    }
    d[args.mepo_stash_cmd].run(args)

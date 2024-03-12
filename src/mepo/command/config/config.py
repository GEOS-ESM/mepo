import subprocess as sp

from state.state import MepoState

from command.config.get    import get
from command.config.set    import set
from command.config.delete import delete
from command.config.print  import print

def run(args):
    d = {
        'get': get,
        'set': set,
        'delete': delete,
        'print': print
    }
    d[args.mepo_config_cmd].run(args)

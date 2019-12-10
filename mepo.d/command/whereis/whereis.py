import os

from state.state import MepoState
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    if args.comp_name:
        verify.valid_components([args.comp_name], allcomps)
        relpath = _get_relative_path(allcomps[args.comp_name]['local'])
        print(relpath)
    else:
        max_name_length = len(max(allcomps, key=len))
        for name, comp in allcomps.items():
            relpath = _get_relative_path(comp['local'])
            _print_where(name, relpath, max_name_length)
        
def _get_relative_path(local_path):
    return os.path.relpath(local_path, os.getcwd())

def _print_where(name, relpath, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, relpath))

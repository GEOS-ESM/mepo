import os

from state.state import MepoState
from utilities import verify

def run(args):
    allrepos = MepoState.read_state()
    if args.repo_name:
        verify.valid_repos([args.repo_name], allrepos.keys())
        relpath = _get_relative_path(allrepos[args.repo_name])
        print(relpath)
    else:
        max_name_length = len(max(allrepos, key=len))
        for name, repo in allrepos.items():
            relpath = _get_relative_path(repo)
            _print_where(name, relpath, max_name_length)
        
def _get_relative_path(repo):
    return os.path.relpath(repo['local'], os.getcwd())

def _print_where(name, relpath, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, relpath))

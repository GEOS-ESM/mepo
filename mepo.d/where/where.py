import os

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        relpath = get_relative_path(repo)
        print_where(name, relpath, max_name_length)

def get_relative_path(repo):
    return os.path.relpath(repo['local'], os.getcwd())

def print_where(name, relpath, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, relpath))

import os

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    relpath = get_relative_path(allrepos[args.repo_name])
    print relpath
    
def get_relative_path(repo):
    return os.path.relpath(repo['local'], os.getcwd())

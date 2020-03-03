import sys
import time
import multiprocessing as mp
import os

from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string

from shutil import get_terminal_size

def run(args):
    print('Diffing...'); sys.stdout.flush()
    allcomps = MepoState.read_state()

    for comp in allcomps:
        result = check_component_diff(comp, args)
        if result:
            print_diff(comp, args, result)

def check_component_diff(comp, args):
    git = GitRepository(comp.remote, comp.local)
    return git.run_diff(args)

def print_diff(comp, args, output):
    columns, lines = get_terminal_size(fallback=(80,20))
    horiz_line = u'\u2500'*columns
    print("{} (location: {}):".format(comp.name,_get_relative_path(comp.local)))
    print()
    for line in output.split('\n'):
        #print('   |', line.rstrip())
        print(line.rstrip())
    print(horiz_line)

def _get_relative_path(local_path):
    return os.path.relpath(local_path, os.getcwd())

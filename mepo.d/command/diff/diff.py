import sys
import time
import multiprocessing as mp
import os

from state.state import MepoState
from repository.git import GitRepository
from utilities import verify

from shutil import get_terminal_size

def run(args):
    print('Diffing...'); sys.stdout.flush()

    allcomps = MepoState.read_state()
    comps2diff = _get_comps_to_diff(args.comp_name, allcomps)

    for comp in comps2diff:
        result = check_component_diff(comp, args)
        if result:
            print_diff(comp, args, result)

def _get_comps_to_diff(specified_comps, allcomps):
    comps_to_diff = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_diff = [x for x in allcomps if x.name in specified_comps]
    return comps_to_diff

def check_component_diff(comp, args):
    git = GitRepository(comp.remote, comp.local)
    return git.run_diff(args, comp.ignore_submodules)

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
    """
    Get the relative path when given a local path.

    local_path: The path to a subrepo as known by mepo (relative to the .mepo directory)
    """

    # This creates a full path on the disk from the root of mepo and the local_path
    full_local_path=os.path.join(MepoState.get_root_dir(),local_path)

    # We return the path relative to where we currently are
    return os.path.relpath(full_local_path, os.getcwd())

import sys
import time
import multiprocessing as mp

from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string
from utilities import colors

def run(args):
    print('Checking status...'); sys.stdout.flush()
    allcomps = MepoState.read_state()
    pool = mp.Pool()
    result = pool.map(check_component_status, allcomps)
    print_status(allcomps, result)

def check_component_status(comp):
    git = GitRepository(comp.remote, comp.local)

    # version_to_string can strip off 'origin/' for display purposes
    # so we save the "internal" name for comparison
    internal_state_branch_name = git.get_version()[0]

    # This can return non "origin/" names for detached head branches
    curr_ver = version_to_string(git.get_version())
    return (curr_ver, internal_state_branch_name, git.check_status())

def print_status(allcomps, result):
    orig_width = len(max([comp.name for comp in allcomps], key=len))
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        current_version, internal_state_branch_name, output = result[index]
        # Check to see if the current tag/branch is the same as the original
        if comp.version.name not in internal_state_branch_name:
            component_name = colors.RED + comp.name + colors.RESET
            width = orig_width + len(colors.RED) + len(colors.RESET)
        else:
            component_name = comp.name
            width = orig_width
        FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
        print(FMT0.format(component_name, current_version))
        if (output):
            for line in output.split('\n'):
                print('   |', line.rstrip())

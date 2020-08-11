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
    revert_branches(allcomps, result)

def check_component_status(comp):
    git = GitRepository(comp.remote, comp.local)
    curr_ver = version_to_string(git.get_version())
    return (curr_ver, git.check_status())

def revert_branches(allcomps, result):
    for index, comp in enumerate(allcomps):
        git = GitRepository(comp.remote, comp.local)
        current_version = result[index][0].split(' ')[1]
        orig_version = comp.version.name
        if current_version != orig_version:
            print(colors.YELLOW + "Reverting " + colors.RESET + "{} to {}".format(comp.name, colors.GREEN + orig_version + colors.RESET))
            git.checkout(comp.version.name)

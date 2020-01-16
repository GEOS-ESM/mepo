import sys
import time
import multiprocessing as mp

from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string

from shutil import get_terminal_size

def run(args):
    print('Diffing...'); sys.stdout.flush()
    allcomps = MepoState.read_state()
    pool = mp.Pool()
    result = pool.map(check_component_diff, allcomps)
    print_diff(allcomps, result)

def check_component_diff(comp):
    git = GitRepository(comp.remote, comp.local)
    curr_ver = version_to_string(git.get_version())
    return (curr_ver, git.run_diff())

def print_diff(allcomps, result):
    columns, lines = get_terminal_size(fallback=(80,20))
    horiz_line = u'\u2500'*columns
    width = len(max([comp.name for comp in allcomps], key=len))
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        current_version, output = result[index]
        if (output):
            #print(horiz_line)
            print("{}:".format(comp.name))
            print()
            for line in output.split('\n'):
                #print('   |', line.rstrip())
                print(line.rstrip())
            print(horiz_line)

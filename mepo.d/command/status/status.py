import sys
import time
import multiprocessing as mp

from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string

def run(args):
    print('Checking status...'); sys.stdout.flush()
    allcomps = MepoState.read_state()
    pool = mp.Pool()
    result = pool.map(check_component_status, allcomps)
    print_status(allcomps, result)

def check_component_status(comp):
    git = GitRepository(comp.remote, comp.local)
    curr_ver = version_to_string(git.get_version())
    return (curr_ver, git.check_status())

def print_status(allcomps, result):
    width = len(max([comp.name for comp in allcomps], key=len))
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        current_version, output = result[index]
        print(FMT0.format(comp.name, current_version))
        if (output):
            for line in output.split('\n'):
                print('   |', line.rstrip())

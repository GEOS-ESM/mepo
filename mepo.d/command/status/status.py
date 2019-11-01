import os
import subprocess as sp

from state.state import MepoState
from command.common import utilities

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        version = utilities.get_current_version(name, repo)
        output = check_status(name, repo)
        print_status(name, version, output, max_name_length)

def check_status(name, repo, verbose=False):
    cmd = 'git -C %s status -s' % repo['local']
    output = sp.check_output(cmd.split())
    return output.rstrip()

def print_status(name, version, output, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, version))
    if (output):
        for line in output.split('\n'):
            print '   |', line.rstrip()

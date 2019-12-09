import os

from state.state import MepoState
from utilities import version
from utilities import shellcmd

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        current_version = version.get_current_s(repo)
        output = check_status(name, repo)
        print_status(name, current_version, output, max_name_length)

def check_status(name, repo, verbose=False):
    cmd = 'git -C {} status -s'.format(repo['local'])
    output = shellcmd.run(cmd.split(), output=True)
    return output.rstrip()

def print_status(name, version, output, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, version))
    if (output):
        for line in output.split('\n'):
            print('   |', line.rstrip())

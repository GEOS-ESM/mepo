import os

from state.state import MepoState
from utilities import version
from utilities import shellcmd

def run(args):
    allcomps = MepoState.read_state()
    max_name_length = len(max(allcomps, key=len))
    for name, comp in allcomps.items():
        current_version = version.get_current_s(comp)
        output = check_status(comp['local'])
        print_status(name, current_version, output, max_name_length)

def check_status(local_path, verbose=False):
    cmd = 'git -C {} status -s'.format(local_path)
    output = shellcmd.run(cmd.split(), output=True)
    return output.rstrip()

def print_status(name, version, output, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, version))
    if (output):
        for line in output.split('\n'):
            print('   |', line.rstrip())

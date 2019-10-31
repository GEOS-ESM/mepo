import os
import subprocess as sp

from state.state import MepoState
from common import utilities

PATH_LEN = 40

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        version = utilities.get_current_version(name, repo)
        relpath = get_relative_path(repo)
        output = check_status(name, repo)
        print_status(name, relpath, version, output, max_name_length)

def check_status(name, repo, verbose=False):
    cmd = 'git -C %s status -s' % repo['local']
    output = sp.check_output(cmd.split())
    return output

def get_relative_path(repo):
    return os.path.relpath(repo['local'], os.getcwd())

def print_status(name, relpath, version, output, width):
    FMT0 = '{:<%s.%ss} | {:<%ss} | {:<s}' % (width, width, PATH_LEN)
    FMT1 = '{:<%s.%ss} | {:<s}' % (width, width)
    FMT2 = '{:^%s.%ss}   {:>%ss} | {:<s}' % (width, width, PATH_LEN)
    if len(relpath) > PATH_LEN:
        print(FMT1.format(name, relpath + ' ...'))
        print(FMT2.format('', '...', version))
    else:
        print(FMT0.format(name, relpath, version))
    if (output):
        for line in output.strip().split('\n'):
            print '   |', line.rstrip()

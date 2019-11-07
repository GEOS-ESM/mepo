import os
import subprocess as sp

from state.state import MepoState
from common import utilities

VER_LEN = 40

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        original = _get_original_version(name, repo)
        current = utilities.get_current_version(name, repo)
        _print_cmp(name, original, current, max_name_length)

def _get_original_version(name, repo):
    version = repo.get('tag')
    version_type = 't'
    if version is None:
        version = repo.get('branch')
        version_type = 'b'
    return '(%s) %s' % (version_type, version)

def _print_cmp(name, orig, cur, name_width):
    FMT_VAL = (name_width, name_width, VER_LEN)
    FMT0 = '{:<%s.%ss} | {:<%ss} | {:<s}' % FMT_VAL
    FMT1 = '{:<%s.%ss} | {:<%ss}' % FMT_VAL
    FMT2 = '{:<%s.%ss} | {:>%ss} | {:<s}' % FMT_VAL
    if len(orig) > VER_LEN:
        print(FMT1.format(name, orig + ' ...'))
        print(FMT2.format('', '...', cur))
    else:
        print(FMT0.format(name, orig, cur))

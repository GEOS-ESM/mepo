import os
import subprocess as sp

from state.state import MepoState
from utilities import version

VER_LEN = 40

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    for name, repo in allrepos.items():
        orig_ver = version.get_original_s(repo)
        cur_ver = version.get_current_s(repo)
        _print_cmp(name, orig_ver, cur_ver, max_name_length)

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

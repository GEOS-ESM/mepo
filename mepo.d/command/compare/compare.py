from state.state import MepoState
from utilities import colors
from utilities.version import version_to_string
from repository.git import GitRepository

VER_LEN = 30

def run(args):
    allcomps = MepoState.read_state()
    max_namelen = len(max([x.name for x in allcomps], key=len))
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        curr_ver = version_to_string(git.get_version())
        orig_ver = version_to_string(comp.version)
        print_cmp(comp.name, orig_ver, curr_ver, max_namelen)

def print_cmp(name, orig, curr, name_width):
    name_blank = ''
    if orig not in curr:
        name = colors.RED + name + colors.RESET
        name_blank = colors.RED + name_blank + colors.RESET
        name_width += len(colors.RED) + len(colors.RESET)
    FMT_VAL = (name_width, name_width, VER_LEN)
    FMT0 = '{:<%s.%ss} | {:<%ss} | {:<s}' % FMT_VAL
    FMT1 = '{:<%s.%ss} | {:<%ss}' % FMT_VAL
    FMT2 = '{:<%s.%ss} | {:>%ss} | {:<s}' % FMT_VAL
    if len(orig) > VER_LEN:
        print(FMT1.format(name, orig + ' ...'))
        print(FMT2.format(name_blank, '...', curr))
    else:
        print(FMT0.format(name, orig, curr))

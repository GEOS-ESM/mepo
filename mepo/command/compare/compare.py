from shutil import get_terminal_size

from mepo.state.state import MepoState
from mepo.utilities import colors
from mepo.utilities.version import version_to_string, sanitize_version_string
from mepo.repository.git import GitRepository

VER_LEN = 30

def run(args):
    allcomps = MepoState.read_state()

    if not any_differing_repos(allcomps):
        print(f'No repositories have changed')
    else:
        max_namelen, max_origlen = calculate_header_lengths(allcomps)
        print_header(max_namelen, max_origlen)
        for comp in allcomps:
            git = GitRepository(comp.remote, comp.local)
            curr_ver = version_to_string(git.get_version(),git)
            orig_ver = version_to_string(comp.version,git)

            # This command is to try and work with git tag oddities
            curr_ver = sanitize_version_string(orig_ver,curr_ver,git)

            print_cmp(comp.name, orig_ver, curr_ver, max_namelen, max_origlen, args.all, args.nocolor, args.wrap)

def any_differing_repos(allcomps):

    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        curr_ver = version_to_string(git.get_version(),git)
        orig_ver = version_to_string(comp.version,git)

        # This command is to try and work with git tag oddities
        curr_ver = sanitize_version_string(orig_ver,curr_ver,git)

        if curr_ver not in orig_ver:
            return True

    return False

def calculate_header_lengths(allcomps):
    names = []
    versions = []
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        names.append(comp.name)
        versions.append(version_to_string(comp.version,git))
    max_namelen = len(max(names, key=len))
    max_origlen = len(max(versions, key=len))
    return max_namelen, max_origlen

def print_header(max_namelen, max_origlen):
    FMT_VAL = (max_namelen, max_namelen, max_origlen)
    FMTHEAD = '{:<%s.%ss} | {:<%ss} | {:<s}' % FMT_VAL
    print(FMTHEAD.format("Repo","Original","Current"))
    print(FMTHEAD.format("-"*80,"-"*max_origlen,"-"*7))

def print_cmp(name, orig, curr, name_width, orig_width, all_repos=False, nocolor=False, wrap=False):
    name_blank = ''
    #if orig not in curr:
    if curr not in orig:
        if not nocolor:
            name = colors.RED + name + colors.RESET
            name_blank = colors.RED + name_blank + colors.RESET
            name_width += len(colors.RED) + len(colors.RESET)
    else:
        # This only prints differing repos unless --all is passed in
        if not all_repos:
            return
    FMT_VAL = (name_width, name_width, orig_width)

    FMT0 = '{:<%s.%ss} | {:<%ss} | {:<s}' % FMT_VAL
    FMT1 = '{:<%s.%ss} | {:<%ss}' % FMT_VAL
    FMT2 = '{:<%s.%ss} | {:>%ss} | {:<s}' % FMT_VAL

    columns, lines = get_terminal_size(fallback=(80,20))

    if (not wrap) and (len(FMT0.format(name, orig, curr)) > columns):
        print(FMT1.format(name, orig + ' ...'))
        print(FMT2.format(name_blank, '...', curr))
    else:
        print(FMT0.format(name, orig, curr))

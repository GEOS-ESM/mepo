from state.state import MepoState
from utilities import colors
from utilities.version import version_to_string
from repository.git import GitRepository
from shutil import get_terminal_size

VER_LEN = 30

def run(args):
    allcomps = MepoState.read_state()
    max_namelen = len(max([x.name for x in allcomps], key=len))
    max_origlen = len(max([version_to_string(x.version) for x in allcomps], key=len))
    print_header(max_namelen, max_origlen)
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        curr_ver = version_to_string(git.get_version())
        orig_ver = version_to_string(comp.version)

        # This command is to try and work with git tag oddities
        curr_ver = sanitize_version_string(orig_ver,curr_ver,git)

        print_cmp(comp.name, orig_ver, curr_ver, max_namelen, max_origlen)

def print_header(max_namelen, max_origlen):
    FMT_VAL = (max_namelen, max_namelen, max_origlen)
    FMTHEAD = '{:<%s.%ss} | {:<%ss} | {:<s}' % FMT_VAL
    print(FMTHEAD.format("Repo","Original","Current"))
    print(FMTHEAD.format("-"*80,"-"*max_origlen,"-"*7))

def print_cmp(name, orig, curr, name_width, orig_width):
    name_blank = ''
    #if orig not in curr:
    if curr not in orig:
        name = colors.RED + name + colors.RESET
        name_blank = colors.RED + name_blank + colors.RESET
        name_width += len(colors.RED) + len(colors.RESET)
    FMT_VAL = (name_width, name_width, orig_width)

    FMT0 = '{:<%s.%ss} | {:<%ss} | {:<s}' % FMT_VAL
    FMT1 = '{:<%s.%ss} | {:<%ss}' % FMT_VAL
    FMT2 = '{:<%s.%ss} | {:>%ss} | {:<s}' % FMT_VAL

    columns, lines = get_terminal_size(fallback=(80,20))

    if len(FMT0.format(name, orig, curr)) > columns:
        print(FMT1.format(name, orig + ' ...'))
        print(FMT2.format(name_blank, '...', curr))
    else:
        print(FMT0.format(name, orig, curr))

def sanitize_version_string(orig,curr,git):
    '''
    This routine tries to figure out if two tags are the same.

    The issue is that git sometimes returns the "wrong" tag in
    the mepo sense. mepo might have checked out tag v1.0.0 but
    if that commit is also tagged with foo, then sometimes mepo
    will say that things have changed because it thinks it's on
    foo.
    '''

    # The trick below only works on tags (I think), so
    # if not a tag, just do nothing for now
    is_tag = '(t)'

    # We pass in space-delimited strings that are:
    #  'type version dh'
    # So let's split into lists...
    orig_list = orig.split()
    curr_list = curr.split()

    # Then pull the types...
    orig_type = orig_list[0]
    curr_type = curr_list[0]

    # Now if a type...
    if orig_type == is_tag and curr_type == is_tag:

        # Pull out the version string...
        orig_ver = orig_list[1]
        curr_ver = curr_list[1]

        # Use rev-list to get the hash of the tag...
        orig_rev = git.rev_list(orig_ver)
        curr_rev = git.rev_list(curr_ver)

        # If they are identical...
        if orig_rev == curr_rev:

            # Replace the curr version with the original to make
            # mepo happy...
            curr_list[curr_list.index(curr_ver)] = orig_ver

            # And then remake the curr string
            curr = ' '.join(curr_list)

    # And return curr
    return curr

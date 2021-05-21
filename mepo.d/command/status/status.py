import sys
import time
import multiprocessing as mp
import atexit

from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string
from utilities import colors

def run(args):
    print('Checking status...'); sys.stdout.flush()
    allcomps = MepoState.read_state()
    pool = mp.Pool()
    atexit.register(pool.close)
    result = pool.map(check_component_status, allcomps)
    print_status(allcomps, result)

def check_component_status(comp):
    git = GitRepository(comp.remote, comp.local)

    # version_to_string can strip off 'origin/' for display purposes
    # so we save the "internal" name for comparison
    internal_state_branch_name = git.get_version()[0]

    # This can return non "origin/" names for detached head branches
    curr_ver = version_to_string(git.get_version())
    orig_ver = version_to_string(comp.version)

    # This command is to try and work with git tag oddities
    curr_ver = sanitize_version_string(orig_ver,curr_ver,git)

    return (curr_ver, internal_state_branch_name, git.check_status())

def print_status(allcomps, result):
    orig_width = len(max([comp.name for comp in allcomps], key=len))
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        current_version, internal_state_branch_name, output = result[index]

        # This should handle tag weirdness...
        if current_version.split()[1] == comp.version.name:
            component_name = comp.name
            width = orig_width
        # Check to see if the current tag/branch is the same as the original...
        # if the above check didn't succeed, we are different.
        elif internal_state_branch_name not in comp.version.name:
            component_name = colors.RED + comp.name + colors.RESET
            width = orig_width + len(colors.RED) + len(colors.RESET)
        else:
            component_name = comp.name
            width = orig_width
        FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
        print(FMT0.format(component_name, current_version))
        if (output):
            for line in output.split('\n'):
                print('   |', line.rstrip())

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

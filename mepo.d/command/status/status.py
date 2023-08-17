import sys
import time
import multiprocessing as mp
import atexit

from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string, sanitize_version_string
from utilities import colors, shellcmd
from command.whereis.whereis import _get_relative_path
import shlex

def run(args):
    print('Checking status...'); sys.stdout.flush()
    allcomps = MepoState.read_state()
    pool = mp.Pool()
    atexit.register(pool.close)
    result = pool.starmap(check_component_status, [(comp, args.ignore_permissions) for comp in allcomps])
    print_status(allcomps, result, args.nocolor, args.hashes)

def check_component_status(comp, ignore):
    git = GitRepository(comp.remote, comp.local)

    # version_to_string can strip off 'origin/' for display purposes
    # so we save the "internal" name for comparison
    internal_state_branch_name = git.get_version()[0]

    # This can return non "origin/" names for detached head branches
    curr_ver = version_to_string(git.get_version(),git)
    orig_ver = version_to_string(comp.version,git)

    # This command is to try and work with git tag oddities
    curr_ver = sanitize_version_string(orig_ver,curr_ver,git)

    return (curr_ver, internal_state_branch_name, git.check_status(ignore))

def print_status(allcomps, result, nocolor=False, hashes=False):
    orig_width = len(max([comp.name for comp in allcomps], key=len))
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        current_version, internal_state_branch_name, output = result[index]
        if hashes:
            comp_path = _get_relative_path(comp.local)
            comp_hash = shellcmd.run(
                cmd=shlex.split(f"git -C {comp_path} rev-parse HEAD"),
                output=True
            ).replace("\n", "")
            current_version = f"{current_version} ({comp_hash})"
        # This should handle tag weirdness...
        if current_version.split()[1] == comp.version.name:
            component_name = comp.name
            width = orig_width
        # Check to see if the current tag/branch is the same as the
        # original... if the above check didn't succeed, we are
        # different and we colorize if asked for
        elif (internal_state_branch_name not in comp.version.name) and not nocolor:
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

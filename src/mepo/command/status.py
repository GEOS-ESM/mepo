"""Current state of mepo managed repositories"""

import time
import shlex
import multiprocessing as mp

from ..state import MepoState
from ..git import GitRepository
from ..utilities import colors
from ..utilities import shellcmd
from ..utilities.version import version_to_string
from ..utilities.version import sanitize_version_string

from .whereis import _get_relative_path


def run(args):
    """Entry point"""
    print("Checking status...", flush=True)
    allcomps = MepoState.read_state()
    # max_width = len(max([comp.name for comp in allcomps], key=len))
    max_width = max([len(comp.name) for comp in allcomps])
    if args.parallel:
        with mp.Pool() as pool:
            result = pool.starmap(
                check_component_status,
                [(comp, args.ignore_permissions) for comp in allcomps],
            )
        print_status(allcomps, result, max_width, args.nocolor, args.hashes)
    else:
        for comp in allcomps:
            result = check_component_status(comp, args.ignore_permissions)
            print_component_status(comp, result, max_width, args.nocolor, args.hashes)


def check_component_status(comp, ignore_permissions):
    """Check the status of a single component"""
    git = GitRepository(comp.remote, comp.local)

    # Older mepo clones will not have ignore_submodules in comp, so
    # we need to handle this gracefully
    try:
        _ignore_submodules = comp.ignore_submodules
    except AttributeError:
        _ignore_submodules = None

    # version_to_string can strip off 'origin/' for display purposes
    # so we save the "internal" name for comparison
    internal_state_branch_name = git.get_version()[0]

    # This can return non "origin/" names for detached head branches
    curr_ver = version_to_string(git.get_version(), git)
    orig_ver = version_to_string(comp.version, git)

    # This command is to try and work with git tag oddities
    curr_ver = sanitize_version_string(orig_ver, curr_ver, git)

    # We also want to see if there are any stashes in the component
    num_stashes = len(git.list_stash().splitlines())

    return (
        curr_ver,
        internal_state_branch_name,
        num_stashes,
        git.check_status(ignore_permissions, _ignore_submodules),
    )


def print_status(allcomps, result, max_width, nocolor=False, hashes=False):
    """Print the status of all components"""
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        print_component_status(comp, result[index], max_width, nocolor, hashes)


def print_component_status(comp, result, width, nocolor=False, hashes=False):
    """Print the status of a single component"""
    current_version, internal_state_branch_name, num_stashes, output = result
    if hashes:
        comp_path = _get_relative_path(comp.local)
        comp_hash = shellcmd.run(
            cmd=shlex.split(f"git -C {comp_path} rev-parse HEAD"), output=True
        ).replace("\n", "")
        current_version = f"{current_version} ({comp_hash})"
    # This should handle tag weirdness...
    if current_version.split()[1] == comp.version.name:
        component_name = comp.name
    # Check to see if the current tag/branch is the same as the
    # original... if the above check didn't succeed, we are
    # different and we colorize if asked for
    elif (internal_state_branch_name not in comp.version.name) and not nocolor:
        component_name = colors.RED + comp.name + colors.RESET
        width += len(colors.RED) + len(colors.RESET)
    else:
        component_name = comp.name

    # If there are stashes, we print the number of stashes in yellow
    if num_stashes:
        stash_str = colors.YELLOW + f"[stashes: {num_stashes}]" + colors.RESET
        print(f"{component_name:<{width}} | {current_version} {stash_str}")
    else:
        print(f"{component_name:<{width}} | {current_version}")
    if output:
        for line in output.split("\n"):
            print("   |", line.rstrip())

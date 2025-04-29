"""Current state of mepo managed repositories"""

import time
import shlex
import multiprocessing as mp

from ..state import MepoState
from ..git import GitRepository
from ..utilities import colors
from ..utilities import shellcmd
from ..utilities import statcolor
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

    return (
        curr_ver,
        internal_state_branch_name,
        git.check_status(ignore_permissions, _ignore_submodules),
    )


def print_status(allcomps, result, max_width, nocolor=False, hashes=False):
    """Print the status of all components"""
    for index, comp in enumerate(allcomps):
        time.sleep(0.025)
        print_component_status(comp, result[index], max_width, nocolor, hashes)


def print_component_status(comp, result, width, nocolor=False, hashes=False):
    """Print the status of a single component"""
    current_version, internal_state_branch_name, output = result
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

    ahead_behind_stash, changes = parse_output(output)
    print(f"{component_name:<{width}} | {current_version}{ahead_behind_stash}")
    for line in changes:
        print("   |", line.rstrip())


def parse_output(output):
    headers = []
    changes = []
    for item in output.splitlines():
        if item.startswith("#"):
            headers.append(item)
        else:
            changes.append(item)
    ahead_behind_stash = parse_headers(headers)
    changes = parse_changed_entries(changes)
    return (ahead_behind_stash, changes)


def parse_headers(headers):
    result = ""
    for header in headers:
        header = header.strip("# ").split()
        if header[0] == "stash":
            num_stashes = header[1]
            result += statcolor.yellow(f" [stashes: {num_stashes}]")
        elif header[0] == "branch.ab":
            ahead = int(header[1].lstrip("+"))
            if ahead > 0:
                result += statcolor.yellow(f" [ahead: {ahead}]")
            behind = int(header[2].lstrip("-"))
            if behind > 0:
                result += statcolor.yellow(f" [behind: {behind}]")
    return result


def parse_changed_entries(changes):
    max_len = 0
    if changes:
        changed_files = [x.split()[-1] for x in changes]
        max_len = len(max(changed_files, key=len))
    for idx, item in enumerate(changes):
        type_ = item.split()[0]
        short_ = item.split()[1]
        if type_ == "1":
            status_ = statcolor.get_ordinary_change_status(short_)
        elif type_ == "2":
            new_file_ = item.split()[-2]
            status_ = statcolor.get_renamed_copied_status(short_, new_file_)
        elif type_ == "?":
            status_ = statcolor.red("untracked file")
        else:
            status_ = statcolor.cyan("unknown") + " (contact mepo maintainer)"
        file_name = item.split()[-1]
        status_string_ = f"{file_name:>{max_len}}: {status_}"
        changes[idx] = status_string_
    return changes

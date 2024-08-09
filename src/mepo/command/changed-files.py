import os

from ..state import MepoState

from ..utilities import verify
from ..utilities.version import version_to_string
from ..utilities.version import sanitize_version_string
from ..git import GitRepository

VER_LEN = 30


def run(args):
    allcomps = MepoState.read_state()

    if any_differing_repos(allcomps):
        comps2diff = _get_comps_to_diff(args.comp_name, allcomps)

        for comp in comps2diff:
            git = GitRepository(comp.remote, comp.local)
            orig_ver = version_to_string(comp.version, git).split()[1]
            orig_type = comp.version.type
            changed_files = git.get_changed_files(
                untracked=True, orig_ver=orig_ver, comp_type=orig_type
            )

            # If there are changed files, print them with the local path
            if changed_files:
                for file in changed_files:
                    if args.full_path:
                        print(os.path.abspath(os.path.join(comp.local, file)))
                    else:
                        print(os.path.join(comp.local, file))


def _get_comps_to_diff(specified_comps, allcomps):
    comps_to_diff = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_diff = [x for x in allcomps if x.name in specified_comps]
    return comps_to_diff


def any_differing_repos(allcomps):
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        curr_ver = version_to_string(git.get_version(), git)
        orig_ver = version_to_string(comp.version, git)

        # This command is to try and work with git tag oddities
        curr_ver = sanitize_version_string(orig_ver, curr_ver, git)

        if curr_ver not in orig_ver:
            return True

    return False

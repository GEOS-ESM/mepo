import multiprocessing as mp

from ..state import MepoState
from ..git import GitRepository
from ..utilities.version import version_to_string
from ..utilities import colors


def run(args):
    print("Checking status...", flush=True)
    allcomps = MepoState.read_state()
    if args.parallel:
        with mp.Pool() as pool:
            result = pool.map(check_component_status, allcomps)
    else:
        result = []
        for comp in allcomps:
            result.append(check_component_status(comp))
    restore_state(allcomps, result)


def check_component_status(comp):
    git = GitRepository(comp.remote, comp.local)
    curr_ver = version_to_string(git.get_version(), git)
    return (curr_ver, git.check_status())


def restore_state(allcomps, result):
    for index, comp in enumerate(allcomps):
        git = GitRepository(comp.remote, comp.local)
        current_version = result[index][0].split(" ")[1]
        orig_version = comp.version.name
        if current_version != orig_version:
            print(
                colors.YELLOW
                + "Restoring "
                + colors.RESET
                + "{} to {} from {}.".format(
                    comp.name,
                    colors.GREEN + orig_version + colors.RESET,
                    colors.RED + current_version + colors.RESET,
                )
            )
            git.checkout(comp.version.name)

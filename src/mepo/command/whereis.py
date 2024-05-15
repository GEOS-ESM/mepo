import os

from ..state import MepoState
from ..utilities import verify


def run(args):
    allcomps = MepoState.read_state()
    if args.comp_name:  # single comp name is specified, print relpath
        if args.comp_name == "_root":
            # _root is a "hidden" allowed argument for whereis to return
            # the root dir of the project. Mainly used by mepo-cd
            print(MepoState.get_root_dir())
        else:
            # Verify that we passed in a good component name
            verify.valid_components(
                [args.comp_name], allcomps, ignore_case=args.ignore_case
            )

            # Create a name to look for according to ignore_case option
            component_to_find = (
                args.comp_name.casefold() if args.ignore_case else args.comp_name
            )

            # Loop over all the components that mepo knows about...
            for comp in allcomps:
                # Create a name to compare to based on ignore_case option
                component_in_allcomps = (
                    comp.name.casefold() if args.ignore_case else comp.name
                )
                # And if they match, print the relative path
                if component_in_allcomps == component_to_find:
                    print(_get_relative_path(comp.local))

    else:  # print relpaths of all comps
        max_namelen = len(max([x.name for x in allcomps], key=len))
        FMT = "{:<%s.%ss} | {:<s}" % (max_namelen, max_namelen)
        for comp in allcomps:
            print(FMT.format(comp.name, _get_relative_path(comp.local)))


def _get_relative_path(local_path):
    """
    Get the relative path when given a local path.

    local_path: The path to a subrepo as known by mepo (relative to the .mepo directory)
    """

    # This creates a full path on the disk from the root of mepo and the local_path
    full_local_path = os.path.join(MepoState.get_root_dir(), local_path)

    # We return the path relative to where we currently are
    return os.path.relpath(full_local_path, os.getcwd())

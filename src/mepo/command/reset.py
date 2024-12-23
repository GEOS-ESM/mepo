import os
import shutil

from ..state import MepoState
from ..utilities.exceptions import NotInRootDirError

from .clone import run as mepo_clone_run

# This command will "reset" the mepo clone. This will delete all
# the subrepos, remove the mepo state directory, and then re-clone all the
# subrepos. This is useful if you want to start over with a fresh clone
# of the project.


def run(args):
    allcomps = MepoState.read_state()

    # Check to see that we are in the root directory of the project
    ## First get the root directory of the project
    rootdir = MepoState.get_root_dir()
    ## Then get the current directory
    curdir = os.getcwd()
    ## Then check that they are the same, if they are not, then throw a NotInRootDirError
    if rootdir != curdir:
        raise NotInRootDirError(
            "Error! As a safety precaution, you must be in the root directory of the project to reset"
        )

    # If we get this far, then we are in the root directory of the project

    # If a user has called this command without the force flag, we
    # will ask them to confirm that they want to reset the project
    if not args.force and not args.dry_run:
        print(
            "Are you sure you want to reset the project? If so, type 'yes' and press enter.",
            end=" ",
        )
        answer = input()
        if answer != "yes":
            print("Reset cancelled.")
            return

    # First, we need to delete all the subrepos
    # Loop over all the components in reverse (since we are deleting them)
    for comp in reversed(allcomps):
        # If the component is the Fixture, then skip it
        if comp.fixture:
            continue
        else:
            # Get the relative path to the component
            relpath = _get_relative_path(comp.local)
            print(f"Removing {relpath}", end="...")
            # Remove the component if not dry run
            if not args.dry_run:
                shutil.rmtree(relpath)
                print("done.")
            else:
                print(f"dry-run only. Not removing {relpath}")

    # Next, we need to remove the .mepo directory
    print("Removing mepo state", end="...")
    if not args.dry_run:
        shutil.rmtree(MepoState.get_dir())
        print("done.")
    else:
        print("dry-run only. Not removing mepo state")

    # If they pass in the --reclone flag, then we will re-clone all the subrepos
    if args.reclone:

        # mepo_clone requires args which is an Argparse Namespace object
        # We will create a new Namespace object with the correct arguments
        # for mepo_clone
        clone_args = type(
            "Namespace",
            (object,),
            {
                "url": None,
                "directory": None,
                "branch": None,
                "registry": None,
                "allrepos": False,
                "style": None,
            },
        )
        if not args.dry_run:
            print("Re-cloning all subrepos")
            mepo_clone_run(clone_args)
            print("Recloning done.")
        else:
            print("Dry-run only. Not re-cloning all subrepos")


def _get_relative_path(local_path):
    """
    Get the relative path when given a local path.

    local_path: The path to a subrepo as known by mepo (relative to the mepo state directory)
    """

    # This creates a full path on the disk from the root of mepo and the local_path
    full_local_path = os.path.join(MepoState.get_root_dir(), local_path)

    # We return the path relative to where we currently are
    return os.path.relpath(full_local_path, os.getcwd())

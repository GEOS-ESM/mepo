import os
import pathlib
from urllib.parse import urlparse

from ..state import MepoState
from ..component import MepoComponent
from ..git import GitRepository
from ..utilities import colors
from ..utilities import mepoconfig
from ..registry import Registry


def run(args):
    """
    Entry point of clone
    First clone the fixture, then recurse over sub-repos and clone
    """
    partial = handle_partial(args.partial)
    clone_fixture(args.url, args.branch, args.directory, partial)

    fixture_dir = os.path.dirname(os.path.abspath(args.registry))
    allcomps = []
    recursive_clone(fixture_dir, partial, allcomps)
    MepoState().write_state(allcomps)  # create mepo state

    if args.allrepos:
        if args.branch is None:
            raise ValueError("allrepos option must be used with a branch/tag")
        for comp in allcomps:
            git = GitRepository(comp.remote, comp.local)
            branch = colors.YELLOW + args.branch + args.RESET
            print(f"Checking out {branch} in {comp.name}")
            git.checkout(args.branch, detach=True)


def handle_partial(arg_partial):
    """
    The partial argument to clone can be set either via command line or
    through .mepoconfig
    partial's default value is None, and possible choices are off/blobless/treeless
    """
    ALLOWED = ["blobless", "treeless"]
    partial = arg_partial
    if partial == "off":
        partial = None  # off => None
    if mepoconfig.has_option("clone", "partial"):  # mepoconfig wins
        partial = mepoconfig.get("clone", "partial")
        if partial not in ALLOWED:
            raise ValueError(f"Invalid partial type [{partial}] in .mepoconfig")
        print(f"Found partial clone type [{partial}] in .mepoconfig")
    return partial


def clone_fixture(arg_url, arg_branch, arg_directory, partial):
    if arg_directory is None:
        p = urlparse(arg_url)
        last_url_node = p.path.rsplit("/")[-1]
        arg_directory = pathlib.Path(last_url_node).stem
    git = GitRepository(arg_url, arg_directory)
    git.clone(arg_branch, partial)
    os.chdir(arg_directory)


def recursive_clone(local_path, partial, complist):
    registry = os.path.join(local_path, "components.yaml")
    if os.path.isfile(registry):
        for name, details in Registry(registry).read_file().items():
            if "local" in details:
                details["local"] = os.path.join(local_path, details["local"])
            comp = MepoComponent().registry_to_component(name, details, None)
            complist.append(comp)
            if "fixture" in details:
                continue
            # if not comp.fixture:
            git = GitRepository(comp.remote, os.path.join(local_path, comp.local))
            version = comp.version.name
            submodules = comp.recurse_submodules
            # According to Git, treeless clones do not interact well with
            # submodules. So if any comp has the recurse option set to True,
            # we do a non-partial clone
            _partial = None if partial == "treeless" and submodules else partial
            git.clone(version, submodules, _partial)
            if comp.sparse:
                git.sparsify(comp.sparse)
            print_clone_info(comp)
            recursive_clone(os.path.join(local_path, comp.local), partial, complist)


def print_clone_info(comp):
    WIDTH = 27
    ver_name_type = f"({comp.version.type}) {comp.version.name}"
    print(f"{comp.name:<{WIDTH}} | {ver_name_type:<s}")

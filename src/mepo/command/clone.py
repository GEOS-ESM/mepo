import os
import pathlib
from urllib.parse import urlparse

try:
    from contextlib import chdir as chdir_context
except ImportError:
    from ..utilities.chdir import chdir as chdir_context

from ..state import MepoState
from ..component import MepoComponent
from ..git import GitRepository
from ..utilities import colors
from ..utilities import mepoconfig
from ..registry import Registry


REGISTRY = "components.yaml"


def run(args):
    """
    Entry point of clone
    1. Clone fixture
    2. Read registry
    3. Clone components
    4. Write state
    """
    validate_args(args)
    arg_partial = handle_partial(args.partial)
    fixture_dir = clone_fixture(args.url, args.branch, args.directory, arg_partial)
    with chdir_context(fixture_dir):
        allcomps = allcomps_from_registry(args.style)
        clone_components(allcomps, arg_partial)
        MepoState().write_state(allcomps)
        if args.allrepos:
            checkout_branch_in_all_repos(allcomps, args.branch)


def clone_components(allcomps, partial):
    max_namelen = max([len(comp.name) for comp in allcomps])
    for comp in allcomps:
        if comp.fixture:
            continue  # not cloning fixture
        git = GitRepository(comp.remote, comp.local)
        version = comp.version.name
        recurse_submodules = comp.recurse_submodules
        # According to Git, treeless clones do not interact well with
        # submodules. So if any comp has the recurse option set to True,
        # we do a non-partial clone
        partial = None if partial == "treeless" and recurse_submodules else partial
        git.clone(version, recurse_submodules, partial)
        if comp.sparse:
            git.sparsify(comp.sparse)
        print_clone_info(comp.name, comp.version, max_namelen)


def checkout_branch_in_all_repos(allcomps, branch):
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        print(f"Checking out {colors.YELLOW + branch + colors.RESET} in {comp.name}")
        try:
            git.checkout(branch, detach=True)
        except Exception as error:
            print(error)


def allcomps_from_registry(dir_style):
    allcomps = []
    assert os.path.isfile(REGISTRY)
    for name, details in Registry(REGISTRY).read_file().items():
        comp = MepoComponent().registry_to_component(name, details, dir_style)
        allcomps.append(comp)
    return allcomps


def validate_args(args):
    if args.allrepos and args.branch is None:
        raise RuntimeError("The allrepos option must be used with a branch/tag")


def handle_partial(partial):
    """
    The "partial" argument to clone can be set either via command line or
    via .mepoconfig. Non-default value set via command line takes precedence.
    The default value of "partial" is None, and possible choices are None/blobless/treeless
    """
    ALLOWED_NON_DEFAULT = ["blobless", "treeless"]
    if partial is None:  # default value from command line
        if mepoconfig.has_option("clone", "partial"):
            partial = mepoconfig.get("clone", "partial")
            if partial not in ALLOWED_NON_DEFAULT:
                raise ValueError(f"Invalid partial type [{partial}] in .mepoconfig")
            print(f"Found partial clone type [{partial}] in .mepoconfig")
    return partial


def clone_fixture(url, branch, directory, partial):
    if directory is None:
        p = urlparse(url)
        last_url_node = p.path.rsplit("/")[-1]
        directory = pathlib.Path(last_url_node).stem
    git = GitRepository(url, directory)
    git.clone(branch, partial)
    return directory


def print_clone_info(comp_name, comp_version, name_width):
    ver_name_type = f"({comp_version.type}) {comp_version.name}"
    print(f"{comp_name:<{name_width}} | {ver_name_type:<s}")

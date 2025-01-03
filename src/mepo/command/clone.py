import os
import shutil
import pathlib
from urllib.parse import urlparse
from types import SimpleNamespace

from .init import run as mepo_init
from ..state import MepoState
from ..state import StateDoesNotExistError
from ..git import GitRepository
from ..utilities import colors
from ..utilities import mepoconfig


def run(args):
    """
    Entry point of clone.

    Multiple ways to run clone
    1. After fixture has been cloned (via git clone)
       a. mepo init
          mepo clone
       b. mepo clone (initializes mepo)
    2. Clone fixture as well
       a. mepo clone <url> [<directory>]
       b. mepo clone -b <branch> <url> [<directory>]

    Steps -
    1. Clone fixture - if url is provided
    2. Read state - initialize mepo (write state) first, if needed
    3. Clone components
    4. Checkout all repos to the specified branch
    """
    CWD = os.getcwd()

    arg_partial = handle_partial(args.partial)

    if args.url is not None:
        fixture_dir = clone_fixture(args.url, args.branch, args.directory, arg_partial)
        os.chdir(fixture_dir)
    allcomps = read_state(args.style, args.registry)
    clone_components(allcomps, arg_partial)
    if args.allrepos:
        checkout_all_repos(allcomps, args.branch)

    os.chdir(CWD)


def handle_partial(partial):
    """
    The `partial` argument to clone can be set either via command line or
    via .mepoconfig. Non-default value set via command line takes precedence.
    The default value of `partial` is None, and possible choices are None/blobless/treeless
    """
    ALLOWED_NON_DEFAULT = ["blobless", "treeless"]
    if partial is None:  # default value from command line
        if mepoconfig.has_option("clone", "partial"):
            partial = mepoconfig.get("clone", "partial")
            if partial not in ALLOWED_NON_DEFAULT:
                raise ValueError(f"Invalid partial type [{partial}] in .mepoconfig")
            print(f"Found partial clone type [{partial}] in .mepoconfig")
    return partial


def clone_fixture(url, branch=None, directory=None, partial=None):
    if directory is None:
        p = urlparse(url)
        last_url_node = p.path.rsplit("/")[-1]
        directory = pathlib.Path(last_url_node).stem
    git = GitRepository(url, directory)
    git.clone(branch, partial)
    return directory


def read_state(arg_style, arg_registry):
    while True:
        try:
            allcomps = MepoState.read_state()
        except StateDoesNotExistError:
            registry = get_registry(arg_registry)
            mepo_init(SimpleNamespace(style=arg_style, registry=registry))
            continue
        break
    return allcomps


def get_registry(arg_registry):
    registry = "components.yaml"
    if arg_registry is not None:
        shutil.copy(arg_registry, os.getcwd())
        registry = os.path.basename(arg_registry)
    return registry


def clone_components(allcomps, partial):
    max_namelen = max([len(comp.name) for comp in allcomps])
    for comp in allcomps:
        if comp.fixture:
            continue  # not cloning fixture
        recurse_submodules = comp.recurse_submodules
        # According to Git, treeless clones do not interact well with
        # submodules. So if any comp has the recurse option set to True,
        # we do a non-partial clone
        partial = None if partial == "treeless" and recurse_submodules else partial
        version = comp.version.name
        version = version.replace("origin/", "")
        git = GitRepository(comp.remote, comp.local)
        git.clone(version, recurse_submodules, partial)
        if comp.sparse:
            git.sparsify(comp.sparse)
        print_clone_info(comp.name, comp.version, max_namelen)


def print_clone_info(comp_name, comp_version, name_width):
    ver_name_type = f"({comp_version.type}) {comp_version.name}"
    print(f"{comp_name:<{name_width}} | {ver_name_type:<s}")


def checkout_all_repos(allcomps, branch):
    if branch is None:
        raise RuntimeError("`allrepos` option must be used with a branch/tag.")
    for comp in allcomps:
        branch_y = colors.YELLOW + branch + colors.RESET
        print(f"Checking out {branch_y} in {comp.name}")
        git = GitRepository(comp.remote, comp.local)
        git.checkout(branch)

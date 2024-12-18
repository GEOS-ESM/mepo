import os
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
    Steps -
    1. Clone fixture - if url is passed
    2. Read state - if state does not exist, initialize mepo (write state) first
    3. Clone components
    4. Checkout all repos to the specified branch
    """
    CWD = os.getcwd()

    if args.branch is not None and args.url is None:
        raise RuntimeError("The branch argument can only be used with a URL")

    arg_partial = handle_partial(args.partial)

    # Step 1 - clone fixture
    if args.url is not None:
        fixture_dir = clone_fixture(args.url, args.branch, args.directory, arg_partial)
        os.chdir(fixture_dir)

    # Step 2 - Read state - if state does not exist, initialize mepo
    while True:
        try:
            allcomps = MepoState.read_state()
        except StateDoesNotExistError:
            registry = get_registry(args.registry)
            mepo_init(SimpleNamespace(style=args.style, registry=registry))
            continue
        break

    # Step 3 - Clone componets
    clone_components(allcomps, arg_partial)

    # Step 4 - Checkout all repos to the specified branch
    # TODO - pchakrab: DO WE REALLY NEED THIS???
    if args.allrepos:
        if args.branch is None:
            raise RuntimeError("`allrepos` option must be used with a branch/tag.")
        checkout_components(allcomps, args.branch)

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


def checkout_components(allcomps, branch):
    for comp in allcomps:
        if comp.fixture:
            continue  # fixture is already on the right branch
        branch_y = colors.YELLOW + args.branch + colors.RESET
        print(f"Checking out {branch_y} in {comp.name}")
        git = GitRepository(comp.remote, comp.local)
        git.checkout(args.branch)


def print_clone_info(comp_name, comp_version, name_width):
    ver_name_type = f"({comp_version.type}) {comp_version.name}"
    print(f"{comp_name:<{name_width}} | {ver_name_type:<s}")

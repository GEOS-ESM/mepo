import os
import pathlib
import shutil
import shlex
from urllib.parse import urlparse

from .init import run as mepo_init_run
from ..state import MepoState
from ..state import StateDoesNotExistError
from ..git import GitRepository
from ..utilities import shellcmd
from ..utilities import colors
from ..utilities import mepoconfig

def run(args):

    # This protects against someone using branch without a URL
    if args.branch and not args.repo_url:
        raise RuntimeError("The branch argument can only be used with a URL")

    if args.allrepos and not args.branch:
        raise RuntimeError("The allrepos option must be used with a branch/tag.")

    # We can get the blobless and treeless options from the config or the args
    if args.partial:
        # We need to set partial to None if it's off, otherwise we use the
        # string. This is safe because argparse only allows for 'off',
        # 'blobless', or 'treeless'
        partial = None if args.partial == 'off' else args.partial
    elif mepoconfig.has_option('clone','partial'):
        allowed = ['blobless','treeless']
        partial = mepoconfig.get('clone','partial')
        if partial not in allowed:
            raise Exception(f'Detected partial clone type [{partial}] from .mepoconfig is not an allowed partial clone type: {allowed}')
        else:
            print(f'Found partial clone type [{partial}] in .mepoconfig')
    else:
        partial = None


    # If you pass in a registry, with clone, it could be outside the repo.
    # So use the full path
    passed_in_registry = False
    if args.registry:
        passed_in_registry = True
        args.registry = os.path.abspath(args.registry)
    else:
        # If we don't pass in a registry, we need to "reset" the arg to the
        # default name because we pass args to mepo_init
        args.registry = 'components.yaml'
    print(f"args.registry: {args.registry}, passed in registry: {passed_in_registry}")

    if args.repo_url:
        p = urlparse(args.repo_url)
        last_url_node = p.path.rsplit('/')[-1]
        url_suffix = pathlib.Path(last_url_node).suffix
        if args.directory:
            local_clone(args.repo_url,args.branch,args.directory,partial)
            os.chdir(args.directory)
        else:
            if url_suffix == '.git':
                git_url_directory = pathlib.Path(last_url_node).stem
            else:
                git_url_directory = last_url_node

            local_clone(args.repo_url,args.branch,git_url_directory,partial)
            os.chdir(git_url_directory)

    # Copy the new file into the repo only if we pass it in
    if passed_in_registry:
        try:
            shutil.copy(args.registry, os.getcwd())
        except shutil.SameFileError as e:
            pass

    # This tries to read the state and if not, calls init,
    # loops back, and reads the state
    while True:
        try:
            allcomps = MepoState.read_state()
        except StateDoesNotExistError:
            mepo_init_run(args)
            continue
        break

    max_namelen = len(max([comp.name for comp in allcomps], key=len))
    for comp in allcomps:
        if not comp.fixture:
            git = GitRepository(comp.remote, comp.local)
            version = comp.version.name
            version = version.replace('origin/','')
            recurse = comp.recurse_submodules

            # According to Git, treeless clones do not interact well with
            # submodules. So we need to see if any comp has the recurse
            # option set to True. If so, we need to clone that comp "normally"

            _partial = None if partial == 'treeless' and recurse else partial

            # We need the type to handle hashes in components.yaml
            type = comp.version.type
            git.clone(version,recurse,type,comp.name,_partial)
            if comp.sparse:
                git.sparsify(comp.sparse)
            print_clone_info(comp, max_namelen)

    if args.allrepos:
        for comp in allcomps:
            if not comp.fixture:
                git = GitRepository(comp.remote, comp.local)
                print("Checking out %s in %s" %
                        (colors.YELLOW + args.branch + colors.RESET,
                        colors.RESET + comp.name + colors.RESET))
                git.checkout(args.branch,detach=True)

def print_clone_info(comp, name_width):
    ver_name_type = '({}) {}'.format(comp.version.type, comp.version.name)
    print('{:<{width}} | {:<s}'.format(comp.name, ver_name_type, width = name_width))

def local_clone(url,branch=None,directory=None,partial=None):
    cmd1 = 'git clone '

    if partial == 'blobless':
        cmd1 += '--filter=blob:none '
    elif partial == 'treeless':
        cmd1 += '--filter=tree:0 '
    else:
        partial = None

    if branch:
        cmd1 += '--branch {} '.format(branch)
    cmd1 += '--quiet {}'.format(url)
    if directory:
        cmd1 += ' "{}"'.format(directory)
    shellcmd.run(shlex.split(cmd1))
    if branch:
        cmd2 = f'git -C {directory} checkout --detach {branch}'
        shellcmd.run(shlex.split(cmd2))

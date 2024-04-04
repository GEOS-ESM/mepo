import os
import pathlib
import shutil
import shlex
from urllib.parse import urlparse

from ..state.state import MepoState
from ..state.state import StateDoesNotExistError
from ..state.component import MepoComponent
from ..git import GitRepository
from ..utilities import shellcmd
from ..utilities import colors
from ..utilities import mepoconfig
from ..registry import Registry

MAX_NAMELEN = 15

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

    root_component_dir = os.path.dirname(os.path.abspath(args.registry))
    all_components = list()
    __recursive_clone(root_component_dir, all_components, partial)
    MepoState().write_state(all_components)

    if args.allrepos:
        for comp in allcomps:
            if not comp.fixture:
                git = GitRepository(comp.remote, comp.local)
                print("Checking out %s in %s" %
                        (colors.YELLOW + args.branch + colors.RESET,
                        colors.RESET + comp.name + colors.RESET))
                git.checkout(args.branch,detach=True)

def __recursive_clone(local_path, complist, partial):
    registry = os.path.join(local_path, "components.yaml")
    if os.path.isfile(registry):
        complist_dict_from_file = Registry(registry).read_file()
        for name, details in complist_dict_from_file.items():
            if "local" in details: # update local path of component
                details["local"] = os.path.join(local_path, details["local"])
            comp = MepoComponent().to_component(name, details, None)
            complist.append(comp)
            if not comp.fixture:
                git = GitRepository(comp.remote, os.path.join(local_path, comp.local))
                version = comp.version.name
                recurse_submodules = comp.recurse_submodules
                # According to Git, treeless clones do not interact well with
                # submodules. So we need to see if any comp has the recurse
                # option set to True. If so, we need to clone that comp "normally"
                # TODO: Add 'partial' abilities
                _partial = None if partial == 'treeless' and recurse else partial
                # We need the type to handle hashes in components.yaml
                _type = comp.version.type
                git.clone(version, recurse_submodules, _type, comp.name, _partial)
                if comp.sparse:
                    git.sparsify(comp.sparse)
                __print_clone_info(comp)
                __recursive_clone(os.path.join(local_path, comp.local), complist, partial)

def __print_clone_info(comp):
    ver_name_type = '({}) {}'.format(comp.version.type, comp.version.name)
    print('{:<{width}} | {:<s}'.format(comp.name, ver_name_type, width = MAX_NAMELEN))

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

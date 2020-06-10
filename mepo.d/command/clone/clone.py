from state.state    import MepoState, StateDoesNotExistError
from repository.git import GitRepository
from command.init   import init as mepo_init
from utilities      import shellcmd
from urllib.parse import urlparse

import os
import pathlib

def run(args):

    if args.repo_url:
        p = urlparse(args.repo_url)
        last_url_node = p.path.rsplit('/')[-1]
        url_suffix = pathlib.Path(last_url_node).suffix
        if url_suffix == '.git':
            git_url_directory = pathlib.Path(last_url_node).stem
        else:
            git_url_directory = last_url_node

        local_clone(args.repo_url)
        os.chdir(git_url_directory)

    # This tries to read the state and if not, calls init,
    # loops back, and reads the state
    while True:
        try:
            allcomps = MepoState.read_state()
        except StateDoesNotExistError:
            mepo_init.run(args)
            continue
        break

    max_namelen = len(max([comp.name for comp in allcomps], key=len))
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        recurse = comp.recurse_submodules
        git.clone(recurse)
        if comp.sparse:
            git.sparsify(comp.sparse)
        git.checkout(comp.version.name)
        print_clone_info(comp, max_namelen)

def print_clone_info(comp, name_width):
    ver_name_type = '({}) {}'.format(comp.version.type, comp.version.name)
    print('{:<{width}} | {:<s}'.format(comp.name, ver_name_type, width = name_width))

def local_clone(url):
    cmd = 'git clone '
    cmd += '--quiet {}'.format(url)
    shellcmd.run(cmd.split())

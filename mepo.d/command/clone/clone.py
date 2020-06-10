from state.state    import MepoState, MepoStateDoesNotExistError
from repository.git import GitRepository
from command.init   import init as mepo_init

def run(args):
    # This tries to read the state and if not, calls init,
    # loops back, and reads the state
    while True:
        try:
            allcomps = MepoState.read_state()
        except MepoStateDoesNotExistError:
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

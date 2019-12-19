from state.state import MepoState
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    max_namelen = len(max([comp.name for comp in allcomps], key=len))
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        git.clone()
        if comp.sparse:
            git.sparsify(comp.sparse)
        git.checkout(comp.version.name)
        print_clone_info(comp, max_namelen)

def print_clone_info(comp, name_width):
    ver_name_type = '({}) {}'.format(comp.version.type, comp.version.name)
    print('{:<{width}} | {:<s}'.format(comp.name, ver_name_type, width = name_width))

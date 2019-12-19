from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2checkout = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2checkout:
        git = GitRepository(comp.remote, comp.local)
        branch = args.branch_name
        if args.b:
            git.create_branch(branch)
            print('+ {}: {}'.format(comp.name, branch))
        git.checkout(branch)

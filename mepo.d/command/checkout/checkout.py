from state.state import MepoState
from utilities import shellcmd
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps.keys())
    comps_co = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_co.items():
        git = GitRepository(comp['remote'], comp['local'])
        branch_name = args.branch_name
        if args.b:
            git.create_branch(branch_name)
            print('+ {}: {}'.format(name, branch_name))
        git.checkout(branch_name)

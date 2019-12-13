from state.state import MepoState
from utilities import shellcmd
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_del = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_del.items():
        git = GitRepository(comp['remote'], comp['local'])
        git.delete_branch(args.branch_name, args.force)
        print('- {}: {}'.format(name, args.branch_name))

from mepo.state.state import MepoState
from mepo.utilities import verify
from mepo.repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2pushst = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2pushst:
        git = GitRepository(comp.remote, comp.local)
        git.push_stash(args.message)
        #print('+ {}'.format(comp.name))
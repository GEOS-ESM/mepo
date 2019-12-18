from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2dev = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2dev:
        git = GitRepository(comp.remote, comp.local)
        if comp.develop is None:
            raise Exception("'develop' branch not specified for {}".format(comp.name))
        git.checkout(comp.develop)
        git.pull()

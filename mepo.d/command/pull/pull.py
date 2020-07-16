from state.state import MepoState
from utilities import verify
from repository.git import GitRepository
from state.component import MepoVersion

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2dev = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2dev:
        git = GitRepository(comp.remote, comp.local)
        is_detached = MepoVersion(*git.get_version()).detached
        if is_detached:
            raise Exception('{} has detached head! Cannot stage.'.format(comp.name))
        else:
            git.pull()

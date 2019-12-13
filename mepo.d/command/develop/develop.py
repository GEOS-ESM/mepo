from state.state import MepoState
from utilities import verify
from utilities import shellcmd
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps.keys())
    comps_dev = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_dev.items():
        git = GitRepository(comp['remote'], comp['local'])
        if 'develop' not in comp:
            raise Exception("'develop' branch not specified for {}".format(name))
        git.checkout(comp['develop'])
        git.pull()

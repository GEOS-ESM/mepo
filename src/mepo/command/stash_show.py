from ..state import MepoState
from ..utilities import verify
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2showst = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2showst:
        git = GitRepository(comp.remote, comp.local)
        result = git.show_stash(args.patch)
        print(result)

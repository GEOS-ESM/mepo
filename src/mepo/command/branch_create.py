from ..state import MepoState
from ..utilities import verify
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2crtbr = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2crtbr:
        git = GitRepository(comp.remote, comp.local)
        git.create_branch(args.branch_name)
        print(f"+ {comp.name}: {args.branch_name}")

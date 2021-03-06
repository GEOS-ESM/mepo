from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2deltg = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2deltg:
        git = GitRepository(comp.remote, comp.local)
        git.delete_tag(args.tag_name)
        print('- {}: {}'.format(comp.name, args.tag_name))

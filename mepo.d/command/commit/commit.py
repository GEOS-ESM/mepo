from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2commit = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2commit:
        git = GitRepository(comp.remote, comp.local)
        staged_files = git.get_staged_files()
        if staged_files:
            git.commit_files(args.message)
        for myfile in staged_files:
            print('+ {}: {}'.format(comp.name, myfile))

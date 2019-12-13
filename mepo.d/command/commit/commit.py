from state.state import MepoState
from utilities import verify
from utilities import shellcmd
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_commit = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_commit.items():
        git = GitRepository(comp['remote'], comp['local'])
        staged_files = git.get_staged_files()
        if staged_files:
            git.commit_files(args.message)
        for myfile in staged_files:
            print('+ {}: {}'.format(name, myfile))

from state.state import MepoState
from repository.git import GitRepository
from utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        print("Fetching %s" %
                 colors.YELLOW + comp.name + colors.RESET)
        git.fetch(args)

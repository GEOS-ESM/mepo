from utilities import verify
from state.state import MepoState
from repository.git import GitRepository
from utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        output = git.push()
        print('----------\nPushed: {}\n----------'.format(comp.name))
        print(output)

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for name in allrepos:
        print name,

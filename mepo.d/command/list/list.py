from state.state import MepoState

def run(args):
    allcomps = MepoState.read_state()
    for name in allcomps:
        print(name, end=' ')
    print()

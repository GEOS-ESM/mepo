from state.state import MepoState

def run(args):
    allrepos = MepoState.initialize(args.config_file)
    print('Initialized mepo!')

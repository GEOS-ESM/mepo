from state.state import MepoState

def run(args):
    allcomps = MepoState.initialize(args.config_file)
    print('Initializing mepo using {}'.format(args.config_file))

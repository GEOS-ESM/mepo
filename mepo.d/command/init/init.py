from state.state import MepoState

def run(args):
    allcomps = MepoState.initialize(args.config,args.develop)
    print('Initializing mepo using {}'.format(args.config))
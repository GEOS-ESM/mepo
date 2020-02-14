from state.state import MepoState

def run(args):
    allcomps = MepoState.initialize(args.config_file,args.develop)
    print('Initialized mepo!')

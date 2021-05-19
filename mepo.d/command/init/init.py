from state.state import MepoState

def run(args):
    allcomps = MepoState.initialize(args.config,args.style)
    print(f'Initializing mepo using {args.config} with {args.style} style.')

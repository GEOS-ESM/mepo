from state.state import MepoState
from utilities import verify
from repository.git import GitRepository
from utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2checkout = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2checkout:
        git = GitRepository(comp.remote, comp.local)
        branch = args.branch_name
        if args.b:
            git.create_branch(branch)
            if not args.quiet:
                #print('+ {}: {}'.format(comp.name, branch))
                print("Creating and checking out branch %s in %s" %
                        (colors.YELLOW + branch + colors.RESET,
                        colors.RESET + comp.name + colors.RESET))
        else:
            if not args.quiet:
                print("Checking out %s in %s" %
                        (colors.YELLOW + branch + colors.RESET,
                        colors.RESET + comp.name + colors.RESET))
        git.checkout(branch)

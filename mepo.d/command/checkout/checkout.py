from state.state import MepoState
from utilities import verify
from repository.git import GitRepository
from utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    comps2checkout = _get_comps_to_list(args.comp_name, allcomps)
    if args.b and comps2checkout == allcomps:
        raise Exception("We do not allow creating branches without specifying specific repos")
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

def _get_comps_to_list(specified_comps, allcomps):
    comps_to_list = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_list = [x for x in allcomps if x.name in specified_comps]
    return comps_to_list


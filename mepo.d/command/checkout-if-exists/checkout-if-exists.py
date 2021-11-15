from state.state import MepoState
from utilities import verify
from repository.git import GitRepository
from utilities import colors

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        branch = args.branch_name
        status = git.verify_branch(branch)

        if status == 0:
            if args.dry_run:
                print("Branch %s exists in %s" %
                        (colors.YELLOW + branch + colors.RESET,
                         colors.RESET + comp.name + colors.RESET))
            else:
                if not args.quiet:
                    print("Checking out branch %s in %s" %
                            (colors.YELLOW + branch + colors.RESET,
                            colors.RESET + comp.name + colors.RESET))
                git.checkout(branch,args.detach)

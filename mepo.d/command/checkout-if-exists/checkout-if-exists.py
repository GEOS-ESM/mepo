from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        branch = args.branch_name
        status = git.verify_branch(branch)

        if status == 0:
            if args.verbose:
                print("Found branch [%s] in repository [%s]" % (branch, comp.name))
            git.checkout(branch)

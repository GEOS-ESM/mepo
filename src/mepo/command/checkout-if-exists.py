from ..state import MepoState
from ..git import GitRepository
from ..utilities import colors


def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        ref_name = args.ref_name
        status, ref_type = git.verify_branch_or_tag(ref_name)

        if status == 0:
            if args.dry_run:
                print(
                    "%s %s exists in %s"
                    % (
                        ref_type,
                        colors.YELLOW + ref_name + colors.RESET,
                        colors.RESET + comp.name + colors.RESET,
                    )
                )
            else:
                if not args.quiet:
                    print(
                        "Checking out %s %s in %s"
                        % (
                            ref_type.lower(),
                            colors.YELLOW + ref_name + colors.RESET,
                            colors.RESET + comp.name + colors.RESET,
                        )
                    )
                git.checkout(ref_name, args.detach)

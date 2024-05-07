from ..state import MepoState
from ..component import MepoVersion
from ..utilities import verify
from ..utilities import colors
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2pull = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2pull:
        git = GitRepository(comp.remote, comp.local)
        name, tYpe, is_detached = MepoVersion(*git.get_version())
        if is_detached:
            raise Exception("{} has detached head! Cannot pull.".format(comp.name))
        else:
            print(
                "Pulling branch %s in %s "
                % (
                    colors.YELLOW + name + colors.RESET,
                    colors.RESET + comp.name + colors.RESET,
                )
            )
            output = git.pull()
            if not args.quiet:
                print(output)

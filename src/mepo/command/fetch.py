from ..state import MepoState
from ..utilities import colors
from ..utilities import verify
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    comps2fetch = _get_comps_to_list(args.comp_name, allcomps)
    for comp in comps2fetch:
        git = GitRepository(comp.remote, comp.local)
        print("Fetching %s" % colors.YELLOW + comp.name + colors.RESET)
        git.fetch(args)


def _get_comps_to_list(specified_comps, allcomps):
    comps_to_list = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_list = [x for x in allcomps if x.name in specified_comps]
    return comps_to_list

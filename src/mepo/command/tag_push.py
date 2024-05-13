from ..state import MepoState
from ..utilities import verify
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2tagpush = _get_comps_to_list(args.comp_name, allcomps)
    for comp in comps2tagpush:
        git = GitRepository(comp.remote, comp.local)
        git.push_tag(args.tag_name, args.force, args.delete)
        if args.delete:
            print(f"Pushed deleted tag {args.tag_name} to {comp.name}")
        else:
            print(f"Pushed tag {args.tag_name} to {comp.name}")


def _get_comps_to_list(specified_comps, allcomps):
    comps_to_list = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_to_list = [x for x in allcomps if x.name in specified_comps]
    return comps_to_list

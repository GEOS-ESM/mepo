from ..state import MepoState


def run(args):
    _end = "\n" if args.one_per_line else " "
    allcomps = MepoState.read_state()
    for comp in allcomps[:-1]:
        print(comp.name, end=_end)
    print(allcomps[-1].name)

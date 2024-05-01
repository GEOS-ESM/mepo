from ..state import MepoState
from ..component import MepoComponent

def run(args):
    allcomps_old = MepoState.read_state()
    MepoState.mepo1_patch_undo()
    allcomps = []
    for comp in allcomps_old:
        # Convert component to dict and then package
        # it as component again . That is needed toavoid pickle trying to use the path to the old
        # component module
        tmp_dict = comp.to_dict(None)
        name = list(tmp_dict)[0]
        comp = tmp_dict[name]
        allcomps.append(MepoComponent().to_component(name, comp, None))
    MepoState.write_state(allcomps)
    print('\nConverted mepo1 state to mepo2\n')

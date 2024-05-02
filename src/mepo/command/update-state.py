from ..state import MepoState
from ..component import MepoComponent

def run(args):
    allcomps_old = MepoState.read_state()
    MepoState.mepo1_patch_undo()
    # Convert component to dict and then package it as component again. That is
    # needed to avoid pickle trying to use the path to the old modules
    allcomps = []
    for comp in allcomps_old:
        tmp_dict = comp.to_registry_format()
        name = list(tmp_dict)[0]
        comp = tmp_dict[name]
        allcomps.append(MepoComponent().to_component(name, comp, None))
    # Write new state
    MepoState.write_state(allcomps)
    print('\nConverted mepo1 state to mepo2\n')

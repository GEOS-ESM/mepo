import os

from ..state import MepoState
from ..component import MepoComponent

def run(args):
    '''Permanently convert mepo1 state to mepo2 state'''
    allcomps_old = MepoState.read_state()
    MepoState.mepo1_patch_undo()
    # Convert component to dict and then package it as component again. That is
    # needed to avoid pickle trying to use the path to the old modules
    allcomps = []
    for comp in allcomps_old:
        # print(comp)
        tmp_dict = comp.to_registry_format()
        tmp_name = list(tmp_dict)[0]
        tmp_details = tmp_dict[tmp_name]
        # This needs to be run from the fixture directory so that
        # MepoComponent::__set_original_version
        # picks the right repo for setting version
        cwd = os.getcwd()
        os.chdir(MepoState.get_root_dir())
        comp_new = MepoComponent().to_component(tmp_name, tmp_details, None)
        os.chdir(cwd)
        allcomps.append(comp_new)
    # Write new state
    MepoState.write_state(allcomps)
    print('\nConverted mepo1 state to mepo2\n')

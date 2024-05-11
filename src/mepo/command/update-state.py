"""Permanently convert mepo1 state to mepo2 state"""

from ..state import MepoState


def run(_):
    """Entry point"""
    if __old_style_exists_but_new_style_does_not():
        # mepo2 style does not exist
        allcomps = MepoState.read_state()
        MepoState.mepo1_patch_undo()
        # Write new state
        MepoState.write_state(allcomps)
        print("\nConverted mepo1 state to mepo2\n")
    else:
        print("Detected mepo2 style state - nothing to do")


def __old_style_exists_but_new_style_does_not():
    if MepoState.state_exists(old_style=True):
        if not MepoState.state_exists(old_style=False):
            return True
    return False

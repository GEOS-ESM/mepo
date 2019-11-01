import os

from state.state import MepoState
from state.history import MepoHistory

def run(args):
    MepoHistory.read_history(MepoState.get_dir())

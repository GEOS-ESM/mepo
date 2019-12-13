import os
import shutil

from state.state import MepoState
from utilities import version
from utilities import shellcmd
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    for name, comp in allcomps.items():
        ver_name, ver_type, _ = version.get_original(comp)
        ver_name_type = '({}) {}'.format(ver_type, ver_name)
        git = GitRepository(comp['remote'], comp['local'])
        git.clone()
        if 'sparse' in comp:
            git.sparsify(comp['sparse'])
            ver_name_type += ' (sparse)'
        if ver_type == 'b': # we want branch in detached head state
            ver_name = 'origin/' + ver_name
        git.checkout(ver_name)
        print('{:<{width}} | {:<s}'.
              format(name, ver_name_type, width = len(max(allcomps, key=len))))

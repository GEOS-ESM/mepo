import os
import shutil

from state.state import MepoState
from utilities import version
from utilities import shellcmd

def run(args):
    allcomps = MepoState.read_state()
    for name, comp in allcomps.items():
        original = version.get_original(comp)
        ver_name_type = '({}) {}'.format(original.type, original.name)
        _clone_component(comp, original.name, original.type)
        if 'sparse' in comp:
            _sparse_checkout(comp)
            ver_name_type += ' (sparse)'
        print('{:<{width}} | {:<s}'.
              format(name, ver_name_type, width = len(max(allcomps, key=len))))
        
def _clone_component(comp, ver_name, ver_type):
    if ver_type == 'b': # for branch, checkout origin/<branch-name> 
        ver_name = 'origin/' + ver_name
    cmd1 = 'git clone {} {}'.format(comp['remote'], comp['local'])
    out1 = shellcmd.run(cmd1.split(), output=True)
    cmd2 = 'git -C {} checkout {}'.format(comp['local'], ver_name)
    out2 = shellcmd.run(cmd2.split(), output=True)
    clone_output = os.path.join(MepoState.get_dir(), 'clone.log')
    with open(clone_output, 'a') as fout:
        fout.write(out1 + out2)
        
def _sparse_checkout(comp):
    local_path = comp['local']
    dst = os.path.join(local_path, '.git', 'info', 'sparse-checkout')
    shutil.copy(comp['sparse'], dst)
    cmd1 = 'git -C {} config core.sparseCheckout true'.format(local_path)
    shellcmd.run(cmd1.split())
    cmd2 = 'git -C {} read-tree -mu HEAD'.format(local_path)
    shellcmd.run(cmd2.split())

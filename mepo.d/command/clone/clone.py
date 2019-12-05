import os
import shutil

from state.state import MepoState
from utilities import version
from utilities import shellcmd

def run(args):
    allrepos = MepoState.read_state()
    for name, repo in allrepos.items():
        original = version.get_original(repo)
        ver_name_type = '({}) {}'.format(original.type, original.name)
        _clone_component(repo, original.name, original.type)
        if 'sparse' in repo:
            _sparse_checkout(repo)
            ver_name_type += ' (sparse)'
        print('{:<{width}} | {:<s}'.
              format(name, ver_name_type, width = len(max(allrepos, key=len))))
        
def _clone_component(repo, ver_name, ver_type):
    if ver_type == 'b': # for branch, checkout origin/<branch-name> 
        ver_name = 'origin/' + ver_name
    cmd1 = 'git clone {} {}'.format(repo['remote'], repo['local'])
    out1 = shellcmd.run(cmd1.split(), output=True)
    cmd2 = 'git -C {} checkout {}'.format(repo['local'], ver_name)
    out2 = shellcmd.run(cmd2.split(), output=True)
    clone_output = os.path.join(MepoState.get_dir(), 'clone.log')
    with open(clone_output, 'a') as fout:
        fout.write(out1 + out2)
        
def _sparse_checkout(repo):
    local_path = repo['local']
    dst = os.path.join(local_path, '.git', 'info', 'sparse-checkout')
    shutil.copy(repo['sparse'], dst)
    cmd1 = 'git -C {} config core.sparseCheckout true'.format(local_path)
    shellcmd.run(cmd1.split())
    cmd2 = 'git -C {} read-tree -mu HEAD'.format(local_path)
    shellcmd.run(cmd2.split())

import os
import shutil
import subprocess as sp

from state.state import MepoState
from utilities import version

def run(args):
    allrepos = MepoState.read_state()
    for name, repo in allrepos.items():
        ver_name, ver_type = version.get_original(repo)
        ver_name_type = '({}) {}'.format(ver_type, ver_name)
        _clone_component(repo, ver_name, ver_type)
        if 'sparse' in repo:
            _sparse_checkout(repo)
            ver_name_type += ' (sparse)'
        print('{:<{width}} | {:<s}'.
              format(name, ver_name_type, width = len(max(allrepos, key=len))))
        
def _clone_component(repo, ver_name, ver_type):
    cmd = 'git clone -b {} {} {}'.format(ver_name, repo['remote'], repo['local'])
    output_file = os.path.join(MepoState.get_dir(), 'clone.log')
    with open(output_file, 'a') as fnull:
        sp.check_call(cmd.split(), stderr=fnull)
        if ver_type == 'b':
            cmd_next = 'git -C {} checkout origin/{}'.format(repo['local'], ver_name)
            sp.check_call(cmd_next.split(), stderr=fnull)
        
def _sparse_checkout(repo):
    local_path = repo['local']
    src = repo['sparse'] # config file for sparsity
    dst = os.path.join(local_path, '.git', 'info', 'sparse-checkout')
    shutil.copy(src, dst)
    cmd1 = 'git -C {} config core.sparseCheckout true'.format(local_path)
    sp.check_output(cmd1.split())
    cmd2 = 'git -C {} read-tree -mu HEAD'.format(local_path)
    sp.check_output(cmd2.split())

import os
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for name, repo in allrepos.items():
        ver_type, ver_name = get_version(repo)
        clone_component(repo, ver_name)
        v_name_type = '(%s) %s' % (ver_type, ver_name)
        print('{:<{width}} | {:<s}'.
              format(name, v_name_type, width = len(max(allrepos, key=len))))

def clone_component(repo, version):
    git_clone(repo['remote'], version, repo['local'])

def get_version(repo):
    vtype = 't'
    vname = repo.get('tag')
    if vname is None:
        vtype = 'b'
        vname = repo.get('branch')
    return (vtype, vname)

def git_clone(url, version, local_path):
    cmd = 'git clone -b %s %s %s' % (version, url, local_path)
    output_file = os.path.join(MepoState.get_dir(), 'clone.log')
    with open(output_file, 'a') as fnull:
        sp.check_call(cmd.split(), stderr=fnull)

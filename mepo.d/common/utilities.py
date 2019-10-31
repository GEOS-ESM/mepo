import os
import subprocess as sp

def get_current_version(name, repo):
    repo_path = repo['local']
    vname, vtype = get_repo_branch_name(repo_path)
    if vname is None:
        vname, vtype = get_repo_tag_name(repo_path)
        if vname is None:
            raise Exception('Could not find branch or tag name for %s' % name)
    return '(%s) %s' % (vtype, vname.strip())

def get_repo_branch_name(repo_path):
    cmd = 'git -C %s symbolic-ref -q --short HEAD' % repo_path
    try:
        with open(os.devnull, 'w') as ferr:
            vname = sp.check_output(cmd.split(), stderr = ferr)
        return (vname, 'b')
    except sp.CalledProcessError:
        return (None, None)

def get_repo_tag_name(repo_path):
    cmd = 'git -C %s describe --tags --exact-match' % repo_path
    try:
        with open(os.devnull, 'w') as ferr:
            vname = sp.check_output(cmd.split(), stderr = ferr)
        return (vname, 't')
    except sp.CalledProcessError:
        return (None, None)

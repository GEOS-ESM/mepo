import os
import json
import subprocess as sp

from Mepo import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for repo in allrepos:
        __check_status(repo)

def __check_status(repo, verbose=False):
    cwd = os.getcwd()
    orig_branch_or_tag = repo['branch'] or repo['tag']
    os.chdir(repo['path'])
    output = sp.check_output('git status -s'.split())
    changes = ''
    if (output):
        changes = 'Y'
    cur_branch_or_tag = __get_current_branch_or_tag(repo['path'])
    print('{:<1s} | {:<14.14s} | {:<30.30s} | {:<30s}'.
          format(changes, repo['name'], orig_branch_or_tag, cur_branch_or_tag))
    os.chdir(cwd)

def __get_current_branch_or_tag(repo_path):
    try:
        b_t_name = sp.check_output('git symbolic-ref -q --short HEAD'.split())
    except sp.CalledProcessError:
        try:
            cmd = 'git describe --tags --exact-match'.split()
            with open(os.devnull, 'w') as ferr:
                b_t_name = sp.check_output(cmd, stderr = ferr)
        except sp.CalledProcessError:
            raise Exception('Neither a tag nor a branch in %s' % repo_path)
    return b_t_name.strip()

import os
import json
import subprocess as sp

from mepo_state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for repo in allrepos:
        __check_status(repo)

def __check_status(repo, verbose=False):
    cwd = os.getcwd()
    orig_branch_or_tag = repo['branch'] or repo['tag']
    os.chdir(repo['path'])
    output = sp.check_output('git status -s'.split())
    print('{:<14.14s} | {:<40.40s} | {:<33s}'.
          format(
              repo['name'],
              os.path.relpath(repo['path'], cwd),
              __get_current_branch_or_tag(repo['path'])))
    if (output):
        for line in output.split('\n'):
            print '   |', line.rstrip()
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

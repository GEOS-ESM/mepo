import os
import json
import subprocess as sp

from mepo_state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for name, repo in allrepos.items():
        __check_status(name, repo)

def __check_status(name, repo, verbose=False):
    cwd = os.getcwd()
    os.chdir(repo['local'])
    output = sp.check_output('git status -s'.split())
    print('{:<14.14s} | {:<40.40s} | {:<33s}'.
          format(name, os.path.relpath(repo['local'], cwd),
                 __get_current_version(repo['local'])))
    if (output):
        for line in output.split('\n'):
            print '   |', line.rstrip()
    os.chdir(cwd)

def __get_current_version(repo_path):
    try:
        version = sp.check_output('git symbolic-ref -q --short HEAD'.split())
        version = '(b) ' + version
    except sp.CalledProcessError:
        try:
            cmd = 'git describe --tags --exact-match'.split()
            with open(os.devnull, 'w') as ferr:
                version = sp.check_output(cmd, stderr = ferr)
            version = '(t) ' + version
        except sp.CalledProcessError:
            raise Exception('Neither a tag nor a branch in %s' % repo_path)
    return version.strip()

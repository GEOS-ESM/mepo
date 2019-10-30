import os
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    max_name_length = len(max(allrepos, key=len))
    FMT = '{:<%s.%ss} | {:<s}' % (max_name_length, max_name_length)
    for name, repo in allrepos.items():
        output = __git_branch(repo, args.all)
        print(FMT.format(name, output[0]))
        for line in output[1:]:
            print(FMT.format('', line))
        
def __git_branch(repo, all):
    cmd = 'git -C %s branch' % repo['local']
    if all:
        cmd += ' -a'
    output = sp.check_output(cmd.split())
    return output.strip().split('\n')

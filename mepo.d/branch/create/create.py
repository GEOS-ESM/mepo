import sys
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for reponame in args.repo_name:
        if reponame not in allrepos:
            raise Exception('invalid repo name [%s]' % reponame)
        __create_branch(reponame, allrepos[reponame], args.branch_name)

def __create_branch(reponame, repo, branch):
    cmd = 'git -C %s branch %s' % (repo['local'], branch)
    sp.check_output(cmd.split())
    print '+ %s: %s' % (reponame, branch)
    

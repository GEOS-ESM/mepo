from state.state import MepoState
from utilities import shellcmd

def run(args):
    allrepos = MepoState.read_state()
    for reponame in args.repo_name:
        if reponame not in allrepos:
            raise Exception('invalid repo name [{}]'.format(reponame))
        _create_branch(reponame, allrepos[reponame], args.branch_name)

def _create_branch(reponame, repo, branch):
    cmd = 'git -C {} branch {}'.format(repo['local'], branch)
    shellcmd.run(cmd.split())
    print('+ {}: {}'.format(reponame, branch))
    

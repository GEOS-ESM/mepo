import subprocess as sp

from state.state import MepoState
from utilities import verify

def run(args):
    allrepos = MepoState.read_state()
    verify.valid_repos(args.repo_name, allrepos.keys())
    repos_commit = {name: allrepos[name] for name in args.repo_name}
    for name, repo in repos_commit.items():
        staged_files = _get_staged_files(repo)
        if staged_files:
            _commit_files(args.message, repo)
            for myfile in staged_files:
                print('+ {}: {}'.format(name, myfile))

def _get_staged_files(repo):
    cmd = 'git -C {} diff --name-only --staged'.format(repo['local'])
    output = sp.check_output(cmd.split()).decode().strip()
    return output.split('\n') if output else []

def _commit_files(commit_message, repo):
    cmd = ['git', '-C', repo['local'], 'commit', '-m', commit_message]
    sp.check_output(cmd)

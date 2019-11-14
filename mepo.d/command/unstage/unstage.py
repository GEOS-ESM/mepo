import re
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    repolist = _get_repos_to_be_staged(args.repo_name, allrepos)
    for name in repolist:
        repo = allrepos[name]
        for myfile in _get_files_to_unstage(repo):
            _unstage_file(myfile, repo)
            print('- {}: {}'.format(name, myfile))

def _get_repos_to_be_staged(specified_repos, allrepos):
    for reponame in specified_repos:
        if reponame not in allrepos:
            raise Exception('Unknown repo name [{}]'.format(reponame))
    if not specified_repos:
        specified_repos = allrepos.keys()
    return specified_repos

def _unstage_file(myfile, repo):
    cmd = 'git -C {} reset -- {}'.format(repo['local'], myfile)
    sp.check_output(cmd.split())

def _get_files_to_unstage(repo):
    cmd = 'git -C {} diff --name-only --staged'.format(repo['local'])
    output = sp.check_output(cmd.split()).decode().strip()
    return output.split('\n') if output else []

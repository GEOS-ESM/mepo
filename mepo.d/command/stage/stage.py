import re
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    repolist = _get_repos_to_be_staged(args.repo, allrepos)
    for name in repolist:
        repo = allrepos[name]
        for myfile in _get_files_to_stage(repo):
            _stage_file(myfile, repo)
            print '+ {}: {}'.format(name, myfile)

def _get_repos_to_be_staged(specified_repos, allrepos):
    for reponame in specified_repos:
        if reponame not in allrepos:
            raise Exception('Unknown repo name [{}]'.format(reponame))
    if not specified_repos:
        specified_repos = allrepos.keys()
    return specified_repos
        
def _stage_file(myfile, repo):
    cmd = 'git -C %s add %s' % (repo['local'], myfile)
    sp.check_output(cmd.split())

def _get_files_to_stage(repo):
    file_list = list()
    file_list.extend(_get_modified_files(repo))
    file_list.extend(_get_untracked_files(repo))
    return file_list

def _get_modified_files(repo):
    cmd = 'git -C {} diff --name-only'.format(repo['local'])
    output = sp.check_output(cmd.split()).strip()
    return output.split('\n') if output else []

def _get_untracked_files(repo):
    cmd = 'git -C {} ls-files --others --exclude-standard'.format(repo['local'])
    output = sp.check_output(cmd.split()).strip()
    return output.split('\n') if output else []

import re
import subprocess as sp

from state.state import MepoState

def run(args):
    repolist = args.repo
    allrepos = MepoState.read_state()
    _sanity_check(repolist, allrepos)
    if not repolist:
        repolist = allrepos.keys()
    for name, repo in allrepos.iteritems():
        if name not in repolist:
            continue
        file_list = _get_files_to_stage(repo)
        print name
        for myfile in file_list:
            _stage_file(myfile, repo)
            print '   staged: {}'.format(myfile)

def _sanity_check(repolist, allrepos):
    for reponame in repolist:
        if reponame not in allrepos:
            raise Exception('Unknown repo name [{}]'.format(reponame))
    
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

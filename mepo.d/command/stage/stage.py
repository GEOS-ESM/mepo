import subprocess as sp

from state.state import MepoState
from utilities import verify
from utilities import version

def run(args):
    allrepos = MepoState.read_state()
    verify.valid_repos(args.repo_name, allrepos.keys())
    repos_stage = {name: allrepos[name] for name in args.repo_name}
    _throw_error_if_repo_has_detached_head(repos_stage)
    for name, repo in repos_stage.items():
        for myfile in _get_files_to_stage(repo):
            _stage_file(myfile, repo)
            print('+ {}: {}'.format(name, myfile))

def _throw_error_if_repo_has_detached_head(repos):
    reponames_detached_head = _get_reponames_with_detached_head(repos)
    if reponames_detached_head:
        raise Exception('Cannot stage in repos {} with Detached HEAD'.format(
            reponames_detached_head))

def _get_reponames_with_detached_head(repos):
    reponames_with_detached_head = list()
    for name, repo in repos.items():
        c_vname, c_vtype, c_detached_head = version.get_current(repo)
        if c_detached_head == 'DH':
            reponames_with_detached_head.append(name)
    return reponames_with_detached_head

def _get_files_to_stage(repo):
    file_list = list()
    file_list.extend(_get_modified_files(repo))
    file_list.extend(_get_untracked_files(repo))
    return file_list

def _get_modified_files(repo):
    cmd = 'git -C {} diff --name-only'.format(repo['local'])
    output = sp.check_output(cmd.split()).decode().strip()
    return output.split('\n') if output else []

def _get_untracked_files(repo):
    cmd = 'git -C {} ls-files --others --exclude-standard'.format(repo['local'])
    output = sp.check_output(cmd.split()).decode().strip()
    return output.split('\n') if output else []

def _stage_file(myfile, repo):
    cmd = 'git -C %s add %s' % (repo['local'], myfile)
    sp.check_output(cmd.split())

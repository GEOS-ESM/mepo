from state.state import MepoState
from utilities import version
from utilities import shellcmd
from utilities import path as utilspath
from config.config_file import ConfigFile

def run(args):
    allrepos = MepoState.read_state()
    for name, repo in allrepos.items():
        _update_repo(repo)
    MepoState.write_state(allrepos)
    allrepos_rel = utilspath.abspath_to_rel(allrepos, MepoState.get_root_dir())
    ConfigFile(args.config_file).write_yaml(allrepos_rel)
    print("State saved to '{}'".format(args.config_file))

def _update_repo(repo):
    curr_ver = version.get_current(repo)
    orig_ver = version.get_original(repo)
    if _save_conditions_are_met(curr_ver, orig_ver):
        _verify_local_and_remote_commit_ids_match(repo)
        repo['branch'] = curr_ver.name
        repo.pop('tag', None)

def _save_conditions_are_met(curr_ver, orig_ver):
    result = False
    if curr_ver != orig_ver:
        assert curr_ver.type == 'b'
        if curr_ver.detached_head != 'DH': # SPECIAL HANDLING
            result = True
    return result

def _verify_local_and_remote_commit_ids_match(repo):
    curr_ver = version.get_current(repo)
    remote_id = _get_remote_latest_commit_id(repo, curr_ver.name)
    local_id = _get_local_latest_commit_id(repo)
    failmsg = "{} (remote commit) != {} (local commit) for {}:{}. Did you try 'mepo push'?"
    if remote_id != local_id:
        name = repo['remote'].split('/')[-1].split('.')[0]
        msg = failmsg.format(remote_id, local_id, name, curr_ver.name)
        raise Exception(msg)

def _get_remote_latest_commit_id(repo, branch):
    cmd = 'git -C {} ls-remote {} refs/heads/{}'.format(repo['local'], repo['remote'], branch)
    output = shellcmd.run(cmd.split(), output=True).strip()
    if not output:
        errmsg = 'Branch {} does not exist on {}'.format(branch, repo['remote'])
        raise Exception(errmsg)
    return output.split()[0]

def _get_local_latest_commit_id(repo):
    cmd = 'git -C {} rev-parse HEAD'.format(repo['local'])
    return shellcmd.run(cmd.split(), output=True).strip()

from state.state import MepoState
from utilities import version
from utilities import shellcmd
from utilities import path as utilspath
from config.config_file import ConfigFile

def run(args):
    allcomps = MepoState.read_state()
    for name, comp in allcomps.items():
        _update_comp(comp)
    MepoState.write_state(allcomps)
    allcomps_rel = utilspath.abspath_to_rel(allcomps, MepoState.get_root_dir())
    ConfigFile(args.config_file).write_yaml(allcomps_rel)
    print("State saved to '{}'".format(args.config_file))

def _update_comp(comp):
    curr_ver = version.get_current(comp)
    orig_ver = version.get_original(comp)
    if _save_conditions_are_met(curr_ver, orig_ver):
        _verify_local_and_remote_commit_ids_match(comp)
        comp['branch'] = curr_ver.name
        comp.pop('tag', None)

def _save_conditions_are_met(curr_ver, orig_ver):
    result = False
    if curr_ver != orig_ver:
        assert curr_ver.type == 'b'
        if curr_ver.detached_head != 'DH': # SPECIAL HANDLING
            result = True
    return result

def _verify_local_and_remote_commit_ids_match(comp):
    curr_ver = version.get_current(comp)
    remote_id = _get_remote_latest_commit_id(comp, curr_ver.name)
    local_id = _get_local_latest_commit_id(comp)
    failmsg = "{} (remote commit) != {} (local commit) for {}:{}. Did you try 'mepo push'?"
    if remote_id != local_id:
        name = comp['remote'].split('/')[-1].split('.')[0]
        msg = failmsg.format(remote_id, local_id, name, curr_ver.name)
        raise Exception(msg)

def _get_remote_latest_commit_id(comp, branch):
    cmd = 'git -C {} ls-remote {} refs/heads/{}'.format(comp['local'], comp['remote'], branch)
    output = shellcmd.run(cmd.split(), output=True).strip()
    if not output:
        errmsg = 'Branch {} does not exist on {}'.format(branch, comp['remote'])
        raise Exception(errmsg)
    return output.split()[0]

def _get_local_latest_commit_id(comp):
    cmd = 'git -C {} rev-parse HEAD'.format(comp['local'])
    return shellcmd.run(cmd.split(), output=True).strip()

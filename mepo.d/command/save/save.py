from state.state import MepoState
from utilities import version
from utilities import shellcmd
from utilities import path as utilspath
from repository.git import GitRepository
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
        assert curr_ver.type == 'b', '{}'.format(curr_ver)
        if not curr_ver.detached: # SPECIAL HANDLING
            result = True
    return result

def _verify_local_and_remote_commit_ids_match(comp):
    curr_ver = version.get_current(comp)
    git = GitRepository(comp['remote'], comp['local'])
    remote_id = git.get_remote_latest_commit_id(curr_ver.name)
    local_id = git.get_local_latest_commit_id()
    failmsg = "{} (remote commit) != {} (local commit) for {}:{}. Did you try 'mepo push'?"
    if remote_id != local_id:
        name = comp['remote'].split('/')[-1].split('.')[0]
        msg = failmsg.format(remote_id, local_id, name, curr_ver.name)
        raise Exception(msg)

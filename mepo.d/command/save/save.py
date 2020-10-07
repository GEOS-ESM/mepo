from state.state import MepoState
from state.component import MepoVersion
from repository.git import GitRepository
from config.config_file import ConfigFile

import os

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        _update_comp(comp)

    MepoState.write_state(allcomps)

    complist = dict()
    relpath_start = MepoState.get_root_dir()
    for comp in allcomps:
        complist.update(comp.to_dict(relpath_start))
    config_file_root_dir=os.path.join(relpath_start,args.config_file)
    ConfigFile(config_file_root_dir).write_yaml(complist)
    print(f"Components written to '{config_file_root_dir}'")

def _update_comp(comp):
    git = GitRepository(comp.remote, comp.local)
    orig_ver = comp.version
    curr_ver = MepoVersion(*git.get_version())
    if _version_has_changed(curr_ver, orig_ver):
        _verify_local_and_remote_commit_ids_match(git, curr_ver.name, comp.name, curr_ver.type)
        comp.version = curr_ver

def _version_has_changed(curr_ver, orig_ver):
    result = False
    if curr_ver != orig_ver:
        if curr_ver.type == 'b':
            assert curr_ver.detached is False, '{}'.format(curr_ver)
            result = True
        elif curr_ver.type == 't':
            result = True
        elif curr_ver.type == 'h':
            result = True
        else:
            raise Exception("This should not happen")
    return result

def _verify_local_and_remote_commit_ids_match(git, curr_ver_name, comp_name, curr_ver_type):
    remote_id = git.get_remote_latest_commit_id(curr_ver_name, curr_ver_type)
    local_id = git.get_local_latest_commit_id()
    failmsg = "{} (remote commit) != {} (local commit) for {}:{}. Did you try 'mepo push'?"
    if remote_id != local_id:
        msg = failmsg.format(remote_id, local_id, comp_name, curr_ver_name)
        raise Exception(msg)

from state.state import MepoState
from utilities import verify
from utilities import version
from utilities import shellcmd

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_stage = {name: allcomps[name] for name in args.comp_name}
    _throw_error_if_comp_has_detached_head(comps_stage)
    for name, comp in comps_stage.items():
        for myfile in _get_files_to_stage(comp):
            _stage_file(myfile, comp['local'])
            print('+ {}: {}'.format(name, myfile))

def _throw_error_if_comp_has_detached_head(comps):
    compnames_detached_head = _get_compnames_with_detached_head(comps)
    if compnames_detached_head:
        raise Exception('Cannot stage in components {} with Detached HEAD'.
                        format(compnames_detached_head))

def _get_compnames_with_detached_head(comps):
    compnames_with_detached_head = list()
    for name, comp in comps.items():
        current = version.get_current(comp)
        if current.detached_head == 'DH':
            compnames_with_detached_head.append(name)
    return compnames_with_detached_head

def _get_files_to_stage(comp):
    file_list = list()
    file_list.extend(_get_modified_files(comp['local']))
    file_list.extend(_get_untracked_files(comp['local']))
    return file_list

def _get_modified_files(local_path):
    cmd = 'git -C {} diff --name-only'.format(local_path)
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output.split('\n') if output else []

def _get_untracked_files(local_path):
    cmd = 'git -C {} ls-files --others --exclude-standard'.format(local_path)
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output.split('\n') if output else []

def _stage_file(myfile, local_path):
    cmd = 'git -C {} add {}'.format(local_path, myfile)
    shellcmd.run(cmd.split())

import re
from utilities import shellcmd

from state.state import MepoState
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    comps_unstage = _get_comps_to_be_unstaged(args.comp_name, allcomps)
    for name, comp in comps_unstage.items():
        local_path = comp['local']
        for myfile in _get_files_to_unstage(local_path):
            _unstage_file(myfile, local_path)
            print('- {}: {}'.format(name, myfile))

def _get_comps_to_be_unstaged(specified_comps, allcomps):
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_unstage = {name: allcomps[name] for name in specified_comps}
    else:
        comps_unstage = allcomps
    return comps_unstage

def _unstage_file(myfile, local_path):
    cmd = 'git -C {} reset -- {}'.format(local_path, myfile)
    shellcmd.run(cmd.split())

def _get_files_to_unstage(local_path):
    cmd = 'git -C {} diff --name-only --staged'.format(local_path)
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output.split('\n') if output else []

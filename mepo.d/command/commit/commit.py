from state.state import MepoState
from utilities import verify
from utilities import shellcmd

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_commit = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_commit.items():
        local_path = comp['local']
        staged_files = _get_staged_files(local_path)
        if staged_files:
            _commit_files(args.message, local_path)
            for myfile in staged_files:
                print('+ {}: {}'.format(name, myfile))

def _get_staged_files(local_path):
    cmd = 'git -C {} diff --name-only --staged'.format(local_path)
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output.split('\n') if output else []

def _commit_files(commit_message, local_path):
    cmd = ['git', '-C', local_path, 'commit', '-m', commit_message]
    shellcmd.run(cmd)

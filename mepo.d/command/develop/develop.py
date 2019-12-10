from state.state import MepoState
from utilities import verify
from utilities import shellcmd

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps.keys())
    comps_dev = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_dev.items():
        if 'develop' not in comp:
            raise Exception("'develop' branch not specified for {}".format(name))
        local_path = comp['local']
        _checkout_branch(local_path, comp['develop'])
        _sync_branch_with_remote(local_path)

def _checkout_branch(local_path, branch):
    cmd = 'git -C {} checkout {}'.format(local_path, branch)
    shellcmd.run(cmd.split())

def _sync_branch_with_remote(local_path):
    cmd = 'git -C {} pull'.format(local_path)
    shellcmd.run(cmd.split())

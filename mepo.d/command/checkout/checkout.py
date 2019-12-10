from state.state import MepoState
from utilities import shellcmd
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps.keys())
    comps_co = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_co.items():
        local_path = comp['local']
        branch_name = args.branch_name
        if args.b:
            _create_branch(local_path, branch_name)
            print('+ {}: {}'.format(name, branch_name))
        _checkout_branch(local_path, branch_name)

def _checkout_branch(local_path, branch):
    cmd = 'git -C {} checkout {}'.format(local_path, branch)
    shellcmd.run(cmd.split())

def _create_branch(local_path, branch):
    cmd = 'git -C {} branch {}'.format(local_path, branch)
    shellcmd.run(cmd.split())

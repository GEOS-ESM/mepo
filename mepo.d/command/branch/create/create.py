from state.state import MepoState
from utilities import shellcmd
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_crt = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_crt.items():
        _create_branch(comp['local'], args.branch_name)
        print('+ {}: {}'.format(name, args.branch_name))

def _create_branch(local_path, branch):
    cmd = 'git -C {} branch {}'.format(local_path, branch)
    shellcmd.run(cmd.split())
    

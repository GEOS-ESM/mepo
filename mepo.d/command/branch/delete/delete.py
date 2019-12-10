from state.state import MepoState
from utilities import shellcmd
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_del = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_del.items():
        _delete_branch(comp['local'], args.branch_name, args.force)
        print('- {}: {}'.format(name, args.branch_name))

def _delete_branch(local_path, branch, force):
    dash_d = '-d'
    if force:
        dash_d = '-D'
    cmd = 'git -C {} branch {} {}'.format(local_path, dash_d, branch)
    shellcmd.run(cmd.split())

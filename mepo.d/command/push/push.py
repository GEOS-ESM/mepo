from utilities import shellcmd

from state.state import MepoState

def run(args):
    allcomps = MepoState.read_state()
    comps_push = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_push.items():
        local_path = comp['local']
        remote_url = comp['remote']
        output = _push_comp(local_path, remote_url)
        print('----------\nPushed: {}\n----------'.format(name))
        print(output)
        
def _push_comp(local_path, remote_url):
    cmd = 'git -C {} push -u {}'.format(local_path, remote_url)
    return shellcmd.run(cmd.split(), output=True).strip()

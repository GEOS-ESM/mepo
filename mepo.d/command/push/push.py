from utilities import shellcmd
from state.state import MepoState
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    comps_push = {name: allcomps[name] for name in args.comp_name}
    for name, comp in comps_push.items():
        git = GitRepository(comp['remote'], comp['local'])
        output = git.push()
        print('----------\nPushed: {}\n----------'.format(name))
        print(output)

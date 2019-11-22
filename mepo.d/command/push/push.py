from utilities import shellcmd

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    repos_push = {name: allrepos[name] for name in args.repo_name}
    for name, repo in repos_push.items():
        _push_repo(repo)
        print('----------\nPushed: {}\n----------\n'.format(name))

def _push_repo(repo):
    cmd = 'git -C {} push -u {}'.format(repo['local'], repo['remote'])
    shellcmd.run(cmd.split())

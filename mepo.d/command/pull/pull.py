from state.state import MepoState
from utilities import shellcmd

def run(args):
    allrepos = MepoState.read_state()
    repos_pull = {name: allrepos[name] for name in args.repo_name}
    for name, repo in repos_pull.items():
        _pull_repo(repo)
        print('----------\nPulled: {}\n----------'.format(name))

def _pull_repo(repo):
    cmd = 'git -C {} pull'.format(repo['local'])
    shellcmd.run(cmd.split())

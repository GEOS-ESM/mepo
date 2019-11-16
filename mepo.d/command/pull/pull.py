import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    repos_pull = {name: allrepos[name] for name in args.repo_name}
    for name, repo in repos_pull.items():
        _pull_repo(repo)
        print('----------\nPulled: {}\n----------\n'.format(name))

def _pull_repo(repo):
    cmd = 'git -C {} pull'.format(repo['local'])
    sp.check_output(cmd.split())

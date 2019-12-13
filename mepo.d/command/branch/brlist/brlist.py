from state.state import MepoState
from utilities import shellcmd
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    max_name_length = len(max(allcomps, key=len))
    FMT = '{:<%s.%ss} | {:<s}' % (max_name_length, max_name_length)
    for name, comp in allcomps.items():
        git = GitRepository(comp['remote'], comp['local'])
        output = git.list_branch(args.all).rstrip().split('\n')
        print(FMT.format(name, output[0]))
        for line in output[1:]:
            print(FMT.format('', line))

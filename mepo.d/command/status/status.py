from state.state import MepoState
from utilities import version
from utilities import shellcmd
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    max_name_length = len(max(allcomps, key=len))
    for name, comp in allcomps.items():
        git = GitRepository(comp['remote'], comp['local'])
        curr_ver = version.get_current_s(comp)
        output = git.check_status()
        print_status(name, curr_ver, output, max_name_length)

def print_status(name, version, output, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, version))
    if (output):
        for line in output.split('\n'):
            print('   |', line.rstrip())

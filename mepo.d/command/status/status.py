from state.state import MepoState
from repository.git import GitRepository
from utilities.version import version_to_string

def run(args):
    allcomps = MepoState.read_state()
    max_namelen = len(max([comp.name for comp in allcomps], key=len))
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        curr_ver = version_to_string(git.get_version())
        output = git.check_status()
        print_status(comp.name, curr_ver, output, max_namelen)

def print_status(name, version, output, width):
    FMT0 = '{:<%s.%ss} | {:<s}' % (width, width)
    print(FMT0.format(name, version))
    if (output):
        for line in output.split('\n'):
            print('   |', line.rstrip())

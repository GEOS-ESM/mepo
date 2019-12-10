from state.state import MepoState
from utilities import shellcmd

def run(args):
    allcomps = MepoState.read_state()
    max_name_length = len(max(allcomps, key=len))
    FMT = '{:<%s.%ss} | {:<s}' % (max_name_length, max_name_length)
    for name, comp in allcomps.items():
        output = __git_branch(comp['local'], args.all).rstrip().split('\n')
        print(FMT.format(name, output[0]))
        for line in output[1:]:
            print(FMT.format('', line))

def __git_branch(local_path, all):
    cmd = 'git -C {} branch'.format(local_path)
    if all:
        cmd += ' -a'
    return shellcmd.run(cmd.split(), output=True)

from ..state import MepoState
from ..git import GitRepository


def run(args):
    allcomps = MepoState.read_state()
    max_namelen = len(max([x.name for x in allcomps], key=len))
    FMT = "{:<%s.%ss} | {:<s}" % (max_namelen, max_namelen)
    for comp in allcomps:
        git = GitRepository(comp.remote, comp.local)
        output = git.list_stash().rstrip().split("\n")
        print(FMT.format(comp.name, output[0]))
        for line in output[1:]:
            print(FMT.format("", line))

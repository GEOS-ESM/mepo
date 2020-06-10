import os

from state.state import MepoState
from utilities import verify

def run(args):
    allcomps = MepoState.read_state()
    if args.comp_name: # single comp name is specified, print relpath
        if args.comp_name == "_root":
            # _root is a "hidden" allowed argument for whereis to return
            # the root dir of the project. Mainly used by mepo-cd
            print(MepoState.get_root_dir())
        else:
            verify.valid_components([args.comp_name], allcomps)
            for comp in allcomps:
                if comp.name == args.comp_name:
                    print(_get_relative_path(comp.local))
    else: # print relpaths of all comps
        max_namelen = len(max([x.name for x in allcomps], key=len))
        FMT = '{:<%s.%ss} | {:<s}' % (max_namelen, max_namelen)
        for comp in allcomps:
            print(FMT.format(comp.name, _get_relative_path(comp.local)))
        
def _get_relative_path(local_path):
    return os.path.relpath(local_path, os.getcwd())

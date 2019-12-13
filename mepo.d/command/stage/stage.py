from state.state import MepoState
from utilities import verify
from utilities import version
from utilities import shellcmd
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps_stage = {name: allcomps[name] for name in args.comp_name}
    _throw_error_if_comp_has_detached_head(comps_stage)
    for name, comp in comps_stage.items():
        git = GitRepository(comp['remote'], comp['local'])
        for myfile in git.get_changed_files(args.untracked):
            git.stage_file(myfile)
            print('+ {}: {}'.format(name, myfile))

def _throw_error_if_comp_has_detached_head(comps):
    compnames_detached_head = _get_compnames_with_detached_head(comps)
    if compnames_detached_head:
        raise Exception('Cannot stage in components {} with Detached HEAD'.
                        format(compnames_detached_head))

def _get_compnames_with_detached_head(comps):
    compnames_with_detached_head = list()
    for name, comp in comps.items():
        current = version.get_current(comp)
        if current.detached:
            compnames_with_detached_head.append(name)
    return compnames_with_detached_head

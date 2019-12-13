from state.state import MepoState
from utilities import shellcmd
from utilities import verify
from repository.git import GitRepository

def run(args):
    allcomps = MepoState.read_state()
    comps_unstage = _get_comps_to_be_unstaged(args.comp_name, allcomps)
    for name, comp in comps_unstage.items():
        git = GitRepository(comp['remote'], comp['local'])
        for myfile in git.get_staged_files():
            git.unstage_file(myfile)
            print('- {}: {}'.format(name, myfile))

def _get_comps_to_be_unstaged(specified_comps, allcomps):
    comps_unstage = allcomps
    if specified_comps:
        verify.valid_components(specified_comps, allcomps)
        comps_unstage = {name: allcomps[name] for name in specified_comps}
    return comps_unstage

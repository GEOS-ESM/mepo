from state.state import MepoState
from utilities import verify
from repository.git import GitRepository
from state.component import MepoVersion

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2stg = [x for x in allcomps if x.name in args.comp_name]
    for comp in comps2stg:
        git = GitRepository(comp.remote, comp.local)
        stage_files(args, comp, git)

def stage_files(args, comp, git):
    curr_ver = MepoVersion(*git.get_version())
    if curr_ver.detached: # detached head
        raise Exception('{} has detached head! Cannot stage.'.format(comp.name))
    for myfile in git.get_changed_files(args.untracked):
        git.stage_file(myfile)
        print('+ {}: {}'.format(comp.name, myfile))

from state.state import MepoState
from utilities import verify
from repository.git import GitRepository

# Popping up an EDITOR is based on https://stackoverflow.com/a/39989442
import os, tempfile, subprocess

def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2commit = [x for x in allcomps if x.name in args.comp_name]

    tf_file = None

    # Pop up an editor if a message is not provided
    if not args.message:
        EDITOR = os.environ.get('EDITOR','vim') # Get the EDITOR
        initial_message = b"" # set up the file

        # Use delete=False to keep the file around as we send the file name to git commit -F
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf_file = tf.name
        tf.write(initial_message)
        tf.flush()
        subprocess.call([EDITOR, tf.name])

    for comp in comps2commit:
        git = GitRepository(comp.remote, comp.local)
        staged_files = git.get_staged_files()
        if staged_files:
            git.commit_files(args.message,tf_file)

        for myfile in staged_files:
            print('+ {}: {}'.format(comp.name, myfile))

    # Now close and by-hand delete the temp file
    if not args.message:
        tf.close()
        os.unlink(tf.name)

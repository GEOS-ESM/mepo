import os
import tempfile
import subprocess

from ..state import MepoState
from ..utilities import verify
from ..git import GitRepository
from ..git import get_editor as get_git_editor

from .stage import stage_files


def run(args):
    allcomps = MepoState.read_state()
    verify.valid_components(args.comp_name, allcomps)
    comps2commit = [x for x in allcomps if x.name in args.comp_name]

    tf_file = None

    # Pop up an editor if a message is not provided
    # Popping up an EDITOR is based on https://stackoverflow.com/a/39989442
    if not args.message:
        EDITOR = get_git_editor()
        initial_message = b""  # set up the file

        # Use delete=False to keep the file around as we send the file name to git commit -F
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf_file = tf.name
        tf.write(initial_message)
        tf.flush()
        subprocess.call([EDITOR, tf.name])

    for comp in comps2commit:
        git = GitRepository(comp.remote, comp.local)
        if args.all:
            stage_files(git, comp, commit=True)

        staged_files = git.get_staged_files()
        if staged_files:
            git.commit_files(args.message, tf_file)

        for myfile in staged_files:
            print("+ {}: {}".format(comp.name, myfile))

    # Now close and by-hand delete the temp file
    if not args.message:
        tf.close()
        os.unlink(tf.name)

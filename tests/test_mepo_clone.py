import os
import io
import shutil
import contextlib
from types import SimpleNamespace

try:
    from contextlib import chdir as contextlib_chdir
except ImportError:
    from mepo.utilities.chdir import chdir as contextlib_chdir

import mepo.command.clone as mepo_clone
import mepo.command.status as mepo_status


FIXTURE_URL = "https://github.com/GEOS-ESM/GEOSfvdycore.git"


def get_mepo_status():
    args = SimpleNamespace(
        ignore_permissions=False,
        nocolor=True,
        hashes=False,
        serial=True,
    )
    with contextlib.redirect_stdout(io.StringIO()) as output:
        mepo_status.run(args)
    return output.getvalue()


def test_mepo_clone_url():
    DIRECTORY = "GEOSfvdycore"
    if os.path.isdir(DIRECTORY):
        shutil.rmtree(DIRECTORY)
    args = SimpleNamespace(
        style="prefix",
        registry=None,
        url=FIXTURE_URL,
        branch=None,
        directory=None,
        partial="blobless",
        allrepos=False,
    )
    mepo_clone.run(args)
    saved_output = """Checking status...
GEOSfvdycore           | (b) main
env                    | (t) v4.29.0 (DH)
cmake                  | (t) v3.51.0 (DH)
ecbuild                | (t) geos/v1.3.0 (DH)
GMAO_Shared            | (t) v1.9.8 (DH)
GEOS_Util              | (t) v2.1.2 (DH)
MAPL                   | (t) v2.48.0 (DH)
FMS                    | (t) geos/2019.01.02+noaff.10 (DH)
FVdycoreCubed_GridComp | (t) v2.12.0 (DH)
fvdycore               | (t) geos/v2.9.0 (DH)
"""
    with contextlib_chdir(DIRECTORY):
        status_output = get_mepo_status()
    assert status_output == saved_output
    shutil.rmtree(DIRECTORY)


def test_mepo_clone_url_branch_directory():
    DIRECTORY = "clone_url_branch_directory"
    if os.path.isdir(DIRECTORY):
        shutil.rmtree(DIRECTORY)
    args = SimpleNamespace(
        style="postfix",
        registry=None,
        url=FIXTURE_URL,
        branch="release/MAPL-v3",
        directory=DIRECTORY,
        partial="blobless",
        allrepos=False,
    )
    mepo_clone.run(args)
    saved_output = """Checking status...
GEOSfvdycore           | (b) release/MAPL-v3
env                    | (t) v4.29.0 (DH)
cmake                  | (t) v3.51.0 (DH)
ecbuild                | (t) geos/v1.3.0 (DH)
GMAO_Shared            | (t) v1.9.8 (DH)
GEOS_Util              | (b) release/MAPL-v3
MAPL                   | (b) release/MAPL-v3
FMS                    | (t) geos/2019.01.02+noaff.10 (DH)
FVdycoreCubed_GridComp | (b) release/MAPL-v3
fvdycore               | (b) geos/release/MAPL-v3
"""
    with contextlib_chdir(DIRECTORY):
        status_output = get_mepo_status()
    assert status_output == saved_output
    shutil.rmtree(DIRECTORY)

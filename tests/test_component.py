import os

from mepo.component import stylize_local_path
from mepo.component import MepoComponent
from mepo.registry import Registry
from mepo.utilities.version import MepoVersion

from _pytest.assertion import truncate

truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def get_registry():
    registry = os.path.join(TEST_DIR, "input", "components.yaml")
    return Registry(registry).read_file()


def get_fvdycore_component():
    comp = MepoComponent()
    comp.name = "fvdycore"
    comp.local = "./src/Components/@FVdycoreCubed_GridComp/@fvdycore"
    comp.remote = "https://github.com/GEOS-ESM/FVdycoreCubed_GridComp.git"
    comp.version = MepoVersion(name="geos/v1.3.0", type="t", detached=True)
    comp.sparse = None
    comp.develop = "geos/develop"
    comp.recurse_submodules = None
    comp.fixture = False
    comp.ignore_submodules = None
    return comp


def get_fvdycore_serialized():
    return {
        "name": "fvdycore",
        "local": "./src/Components/@FVdycoreCubed_GridComp/@fvdycore",
        "remote": "https://github.com/GEOS-ESM/FVdycoreCubed_GridComp.git",
        "version": ["geos/v1.3.0", "t", True],
        "sparse": None,
        "develop": "geos/develop",
        "recurse_submodules": None,
        "fixture": False,
        "ignore_submodules": None,
    }


def test_stylize_local_path():
    local_path = "./src/Shared/@GMAO_Shared/@GEOS_Util"
    output = stylize_local_path(local_path, None)
    assert output == local_path
    output = stylize_local_path(local_path, "prefix")
    assert output == local_path
    output = stylize_local_path(local_path, "naked")
    assert output == "./src/Shared/@GMAO_Shared/GEOS_Util"
    output = stylize_local_path(local_path, "postfix")
    assert output == "./src/Shared/@GMAO_Shared/GEOS_Util@"


def test_MepoComponent():
    registry = get_registry()
    complist = list()
    for name, comp in registry.items():
        if name == "fvdycore":
            fvdycore = MepoComponent().registry_to_component(name, comp, None)
    assert fvdycore == get_fvdycore_component()
    assert fvdycore.serialize() == get_fvdycore_serialized()

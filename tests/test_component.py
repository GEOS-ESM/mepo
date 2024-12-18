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
    return MepoComponent(
        name="fvdycore",
        local="./src/Components/@FVdycoreCubed_GridComp/@fvdycore",
        remote="https://github.com/GEOS-ESM/GFDL_atmos_cubed_sphere.git",
        version=MepoVersion(name="geos/v1.3.0", type="t", detached=True),
        sparse=None,
        develop="geos/develop",
        recurse_submodules=None,
        fixture=False,
        ignore_submodules=None,
    )


def get_fvdycore_serialized():
    return {
        "name": "fvdycore",
        "local": "./src/Components/@FVdycoreCubed_GridComp/@fvdycore",
        "remote": "https://github.com/GEOS-ESM/GFDL_atmos_cubed_sphere.git",
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
    fvdycore_serialized = fvdycore.serialize()
    remote = fvdycore_serialized["remote"]
    fvdycore_serialized["remote"] = remote.replace(
        "git@github.com:", "https://github.com/"
    )
    assert fvdycore_serialized == get_fvdycore_serialized()

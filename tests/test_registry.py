import os

from mepo.registry import Registry

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def get_ecbuild_details():
    return {
        "local": "./@cmake/@ecbuild",
        "remote": "../ecbuild.git",
        "tag": "geos/v1.2.0",
    }


def test_registry():
    registry = os.path.join(TEST_DIR, "input", "components.yaml")
    a = Registry(registry).read_file()
    assert a["ecbuild"] == get_ecbuild_details()

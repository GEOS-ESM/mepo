import json
import os

import pytest

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


@pytest.mark.parametrize("suffix", [".yaml", ".json"])
@pytest.mark.parametrize(
    "count, message",
    [
        (0, "At least one fixture must be defined in the registry"),
        (2, "Only one fixture can be defined in the registry, found 2"),
    ],
)
def test_registry_invalid_fixture_count(tmp_path, suffix, count, message):
    components = {"ecbuild": get_ecbuild_details()}
    components.update({f"fixture{i}": {"fixture": True} for i in range(count)})
    registry = tmp_path / f"components{suffix}"
    registry.write_text(json.dumps(components))

    with pytest.raises(ValueError, match=f"^{message}$"):
        Registry(registry).read_file()

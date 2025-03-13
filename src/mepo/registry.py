import yaml
import json
import pathlib

from .utilities.exceptions import SuffixNotRecognizedError


# From https://github.com/yaml/pyyaml/issues/127#issuecomment-525800484
class AddBlankLinesDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


class Registry:
    """Class implementing reading, writing and validating a mepo registry"""

    __slots__ = ["__filename", "__filetype"]

    def __init__(self, filename):
        self.__filename = filename
        suffix_list = [".yaml", ".json", ".cfg"]
        file_suffix = pathlib.Path(filename).suffix
        if file_suffix in suffix_list:
            self.__filetype = file_suffix[1:]
        else:
            raise SuffixNotRecognizedError(f"suffix {file_suffix} not supported")

    def __validate(self, d, extensions):
        git_tag_types = {"branch", "tag", "hash"}
        num_fixtures = 0
        for k, v in d.items():
            if "fixture" in v:
                assert v["fixture"] is True
                num_fixtures += 1
                v_keys = list(v.keys())
                required_v_keys = ["fixture", "develop"]
                # For a fixture develop is a required key, extends is optional
                assert v_keys in (required_v_keys, required_v_keys + ["extends"])
                if "extends" in v_keys:  # no other components allowed
                    assert len(d) == 1, "Only a fixture is allowed when extending"
                    assert extensions is not None
            else:
                # For a non-fixture, one and only one of branch/tag/hash allowed
                xsection = git_tag_types.intersection(set(v.keys()))
                if len(xsection) != 1:
                    raise ValueError(f"{k} needs one and only one of {git_tag_types}")
        assert num_fixtures == 1  # Can have one and only one fixture

    def read_file(self):
        """Call read_yaml, read_json etc. using dispatch pattern"""
        return getattr(self, "read_" + self.__filetype)()

    def read_yaml(self):
        """Read yaml registry and return a dict containing contents"""
        with open(self.__filename, "r") as fin:
            d = yaml.safe_load(fin)
        extensions = d.pop("extensions", {})
        overrides = d.pop("overrides", {})
        self.__validate(d, extensions)
        return (d, extensions, overrides)

    def read_json(self):
        """Read json registry and return a dict containing contents"""
        with open(self.__filename, "r") as fin:
            d = json.load(fin)
        extensions = d.pop("extensions", None)
        overrides = d.pop("overrides")
        self.__validate(d, extensions)
        return (d, extensions, overrides)

    def read_cfg(self):
        """Read python registry and return a dict containing contents"""
        raise NotImplementedError("Reading of cfg file has not yet been implemented")

    def write_yaml(self, d):
        """Dump dict d into a yaml file"""

        with open(self.__filename, "w") as fout:
            yaml.dump(d, fout, sort_keys=False, Dumper=AddBlankLinesDumper)

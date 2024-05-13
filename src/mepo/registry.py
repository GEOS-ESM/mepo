import yaml
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


class Registry(object):

    __slots__ = ["__filename", "__filetype"]

    def __init__(self, filename):
        self.__filename = filename
        SUFFIX_LIST = [".yaml", ".json", ".cfg"]
        file_suffix = pathlib.Path(filename).suffix
        if file_suffix in SUFFIX_LIST:
            self.__filetype = file_suffix[1:]
        else:
            raise SuffixNotRecognizedError(
                "suffix {} not supported".format(file_suffix)
            )

    def __validate(self, d):
        git_tag_types = {"branch", "tag", "hash"}
        num_fixtures = 0
        for k, v in d.items():
            if "fixture" in v:
                # In case of a fixture, develop is the only additional key
                num_fixtures += 1
                assert list(v.keys()) == ["fixture", "develop"]
            else:
                # For non-fixture, one and only one of branch/tag/hash allowed
                xsection = git_tag_types.intersection(set(v.keys()))
                if len(xsection) != 1:
                    raise ValueError(f"{k} needs one and only one of {git_tag_types}")
        # Can have one and only one fixture
        assert num_fixtures == 1

    def read_file(self):
        """Call read_yaml, read_json etc. using dispatch pattern"""
        return getattr(self, "read_" + self.__filetype)()

    def read_yaml(self):
        """Read yaml registry and return a dict containing contents"""
        import yaml

        with open(self.__filename, "r") as fin:
            d = yaml.safe_load(fin)
        self.__validate(d)
        return d

    def read_json(self):
        """Read json registry and return a dict containing contents"""
        import json

        with open(self.__filename, "r") as fin:
            d = json.load(fin)
        self.__validate(d)
        return d

    def read_cfg(self):
        """Read python registry and return a dict containing contents"""
        raise NotImplementedError("Reading of cfg file has not yet been implemented")

    def write_yaml(self, d):
        """Dump dict d into a yaml file"""
        import yaml

        with open(self.__filename, "w") as fout:
            yaml.dump(d, fout, sort_keys=False, Dumper=AddBlankLinesDumper)

import os
import shlex

from urllib.parse import urljoin

from .utilities import shellcmd
from .utilities.version import MepoVersion

# This will be used to store the "final nodes" from each subrepo
original_final_node_list = []


class MepoComponent(object):

    __slots__ = [
        "name",
        "local",
        "remote",
        "version",
        "sparse",
        "develop",
        "recurse_submodules",
        "fixture",
        "ignore_submodules",
    ]

    def __init__(self):
        self.name = None
        self.local = None
        self.remote = None
        self.version = None
        self.sparse = None
        self.develop = None
        self.recurse_submodules = None
        self.fixture = None
        self.ignore_submodules = None

    def __repr__(self):
        # Older mepo clones will not have ignore_submodules in comp, so
        # we need to handle this gracefully
        try:
            _ignore_submodules = self.ignore_submodules
        except AttributeError:
            _ignore_submodules = None

        return (
            f"{self.name} -\n"
            f"  local: {self.local}\n"
            f"  remote: {self.remote}\n"
            f"  version: {self.version}\n"
            f"  sparse: {self.sparse}\n"
            f"  develop: {self.develop}\n"
            f"  recurse_submodules: {self.recurse_submodules}\n"
            f"  fixture: {self.fixture}\n"
            f"  ignore_submodules: {_ignore_submodules}"
        )

    def __set_original_version(self, comp_details):
        if self.fixture:
            cmd_if_branch = "git symbolic-ref HEAD"
            # Have to use 'if not' since 0 is a good status
            if not shellcmd.run(cmd_if_branch.split(), status=True):
                output = shellcmd.run(cmd_if_branch.split(), output=True).rstrip()
                ver_name = output.replace("refs/heads/", "")
                ver_type = "b"
                is_detached = False
            else:
                # On some CI systems, git is handled oddly. As such, sometimes
                # tags aren't found due to shallow clones
                cmd_for_tag = "git describe --tags"
                # Have to use 'if not' since 0 is a good status
                if not shellcmd.run(cmd_for_tag.split(), status=True):
                    ver_name = shellcmd.run(cmd_for_tag.split(), output=True).rstrip()
                    ver_type = "t"
                    is_detached = True
                else:
                    # Per internet, describe always should always work, though mepo
                    # will return weirdness (a grafted branch, probably a hash)
                    cmd_for_always = "git describe --always"
                    ver_name = shellcmd.run(
                        cmd_for_always.split(), output=True
                    ).rstrip()
                    ver_type = "h"
                    is_detached = True
        else:
            if comp_details.get("branch", None):
                # SPECIAL HANDLING of 'detached head' branches
                ver_name = "origin/" + comp_details["branch"]
                ver_type = "b"
                # we always detach branches from components.yaml
                is_detached = True
            elif comp_details.get("hash", None):
                # Hashes don't have to exist
                ver_name = comp_details["hash"]
                ver_type = "h"
                is_detached = True
            else:
                ver_name = comp_details["tag"]  # 'tag' key has to exist
                ver_type = "t"
                is_detached = True
        self.version = MepoVersion(ver_name, ver_type, is_detached)

    def registry_to_component(self, comp_name, comp_details, comp_style):
        self.name = comp_name
        self.fixture = comp_details.get("fixture", False)
        # local/remote - start
        if self.fixture:
            self.local = "."
            self.remote = get_current_remote_url()
        else:
            # Assume the flag for repostories is commercial-at
            repo_flag = "@"

            # To make it easier to loop over the local path, split into a list
            local_list = splitall(comp_details["local"])

            # The last node of the path is what we will decorate
            last_node = local_list[-1]

            # Add that final node to a list
            original_final_node_list.append(last_node)

            # Now we need to decorate all the final nodes since we can have
            # nested repos with mepo
            for item in original_final_node_list:
                try:
                    # Find the index of every "final node" in a local path
                    # for nesting
                    index = local_list.index(item)

                    # Decorate all final nodes
                    local_list[index] = decorate_node(item, repo_flag, comp_style)
                except ValueError:
                    pass

            # Now pull the list of nodes back into a path
            self.local = os.path.join(*local_list)
            # print(f'final self.local: {self.local}')

            self.remote = comp_details["remote"]
            if self.remote.startswith("../"):
                self.remote = urljoin(get_current_remote_url() + "/", self.remote)
        # local/remote - end

        # Optionals
        self.sparse = comp_details.get("sparse", None)
        self.develop = comp_details.get("develop", None)
        self.recurse_submodules = comp_details.get("recurse_submodules", None)
        self.ignore_submodules = comp_details.get("ignore_submodules", None)
        self.__set_original_version(comp_details)

        return self

    def to_registry_format(self):
        details = dict()
        # Fixtures are allowed exactly two entries
        if self.fixture:
            details["fixture"] = self.fixture
            if self.develop:
                details["develop"] = self.develop
        else:
            details["local"] = self.local
            details["remote"] = self.remote
            if self.version.type == "t":
                details["tag"] = self.version.name
            elif self.version.type == "h":
                details["hash"] = self.version.name
            else:  # if not tag or hash, version has to be a branch
                if (
                    self.version.detached
                ):  # SPECIAL HANDLING of 'detached head' branches
                    details["branch"] = self.version.name.replace("origin/", "")
                else:
                    details["branch"] = self.version.name
            if self.sparse:
                details["sparse"] = self.sparse
            if self.develop:
                details["develop"] = self.develop
            if self.recurse_submodules:
                details["recurse_submodules"] = self.recurse_submodules
            if self.ignore_submodules:
                details["ignore_submodules"] = self.ignore_submodules
        return {self.name: details}

    def deserialize(self, d):
        for k in self.__slots__:
            v = d[k]
            if k == "version":
                # list -> namedtuple
                v = MepoVersion(*v)  # * for arg unpacking
            setattr(self, k, v)
        return self

    def serialize(self):
        d = {}
        for k in self.__slots__:
            v = getattr(self, k)
            if k == "version":
                # namedtuple -> list
                v = list(v)
            d.update({k: v})
        return d


def get_current_remote_url():
    cmd = "git remote get-url origin"
    output = shellcmd.run(shlex.split(cmd), output=True).strip()
    return output


def decorate_node(item, flag, style):
    # If we do not pass in a style...
    if not style:
        # Just use what's in components.yaml
        return item
    # else use the style
    else:
        item = item.replace(flag, "")
        if style == "naked":
            output = item
        elif style == "prefix":
            output = flag + item
        elif style == "postfix":
            output = item + flag
        return output


# From https://learning.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

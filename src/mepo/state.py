import os
import sys
import json
import glob
import pickle

from pathlib import Path

from .registry import Registry
from .component import MepoComponent
from .utilities import shellcmd
from .utilities import colors
from .utilities.exceptions import StateDoesNotExistError
from .utilities.exceptions import StateAlreadyInitializedError
from .utilities.chdir import chdir as mepo_chdir
from .utilities.version import MepoVersion


class MepoState(object):

    __state_dir_name = ".mepo"
    __state_fileptr_name = "state.json"

    @staticmethod
    def get_parent_dirs():
        mypath = os.getcwd()
        parentdirs = [mypath]
        while mypath != "/":
            mypath = os.path.dirname(mypath)
            parentdirs.append(mypath)
        return parentdirs

    @classmethod
    def get_dir(cls):
        """Return location of mepo state dir"""
        for mydir in cls.get_parent_dirs():
            state_dir = os.path.join(mydir, cls.__state_dir_name)
            if os.path.exists(state_dir):
                return state_dir
        raise OSError("mepo state dir [.mepo] does not exist")

    @classmethod
    def get_root_dir(cls):
        """Return fixture (root) directory that contains mepo state dir"""
        return os.path.dirname(cls.get_dir())

    @classmethod
    def get_file(cls):
        """Return location of mepo state file"""
        state_file = os.path.join(cls.get_dir(), cls.__state_fileptr_name)
        if os.path.exists(state_file):
            return state_file
        raise OSError("mepo state file [%s] does not exist" % state_file)

    @classmethod
    def __state_exists(cls):
        try:
            cls.get_file()
            return True
        except OSError:
            return False

    @classmethod
    def initialize(cls, project_registry, directory_style):
        if cls.__state_exists():
            raise StateAlreadyInitializedError("Error! mepo state already exists")
        input_components = Registry(project_registry).read_file()
        complist = list()
        for name, comp in input_components.items():
            complist.append(MepoComponent().to_component(name, comp, directory_style))
        cls.write_state(complist)

    @staticmethod
    def __mepo1_patch():
        """
        mepo1 to mepo2 includes renaming of directories
        Since pickle requires that "the class definition must be importable
        and live in the same module as when the object was stored", we need to
        patch sys.modules to be able to read mepo1 state
        """
        print(
            colors.YELLOW
            + "Converting mepo1 state to mepo2 state\n"
            + "Run <mepo update-state> to permanently convert to mepo2 state"
            + colors.RESET
        )
        import mepo

        sys.modules["state"] = mepo.state
        sys.modules["state.component"] = mepo.component
        sys.modules["utilities"] = mepo.utilities

    @staticmethod
    def mepo1_patch_undo():
        """
        Undo changes made my __mepo1_patch(). Called during <mepo update-state>
        """
        import mepo

        entries_to_remove = ["state", "state.component", "utilities"]
        for key in entries_to_remove:
            sys.modules.pop(key, None)

    @classmethod
    def read_state(cls):
        if not cls.__state_exists():
            raise StateDoesNotExistError("Error! mepo state does not exist")
        with open(cls.get_file(), "r") as fin:
            allcomps_d = json.load(fin)
        # List of dicts -> state (list of MepoComponent objects)
        allcomps = []
        for comp in allcomps_d:
            comp["version"] = MepoVersion(*comp["version"])
            allcomps.append(MepoComponent().to_component_1(comp))
        return allcomps

    @classmethod
    def write_state(cls, allcomps):
        if cls.__state_exists():
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), "state.*.json")
            states = [os.path.basename(x) for x in glob.glob(os.path.join(pattern))]
            new_state_id = max([int(x.split(".")[1]) for x in states]) + 1
            state_file_name = "state." + str(new_state_id) + ".json"
        else:
            state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
            os.mkdir(state_dir)
            state_file_name = "state.0.json"
        new_state_file = os.path.join(state_dir, state_file_name)
        allcomps_d = []
        for comp in allcomps:
            allcomps_d.append(comp.to_dict())
        with open(new_state_file, "w") as fout:
            json.dump(allcomps_d, fout)
        state_fileptr = cls.__state_fileptr_name
        state_fileptr_fullpath = os.path.join(state_dir, state_fileptr)
        if os.path.isfile(state_fileptr_fullpath):
            os.remove(state_fileptr_fullpath)
        # os.symlink(new_state_file, state_fileptr_fullpath)
        with mepo_chdir(state_dir):
            os.symlink(state_file_name, state_fileptr)

import os
import sys
import json
import glob
import stat
import pickle

from .registry import Registry
from .component import MepoComponent
from .utilities import colors
from .utilities.exceptions import StateDoesNotExistError
from .utilities.exceptions import StateAlreadyInitializedError
from .utilities.chdir import chdir as mepo_chdir


class MepoState(object):

    __state_dir_name = ".mepo"
    __state_fileptr_name = "state.json"
    __state_fileptr_name_old = "state.pkl"

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
    def get_file(cls, old_style=False):
        """Return location of mepo state file"""
        if old_style:
            fileptr_name = cls.__state_fileptr_name_old
        else:
            fileptr_name = cls.__state_fileptr_name
        state_file = os.path.join(cls.get_dir(), fileptr_name)
        if os.path.exists(state_file):
            return state_file
        else:
            raise OSError(f"mepo state file [{state_file}] does not exist")

    @classmethod
    def state_exists(cls, old_style=False):
        try:
            cls.get_file(old_style)
            return True
        except OSError:
            return False

    @classmethod
    def initialize(cls, project_registry, directory_style):
        if cls.state_exists():
            raise StateAlreadyInitializedError("Error! mepo state already exists")
        input_components = Registry(project_registry).read_file()
        complist = list()
        for name, comp in input_components.items():
            complist.append(
                MepoComponent().registry_to_component(name, comp, directory_style)
            )
        cls.write_state(complist)

    @staticmethod
    def __mepo1_patch():
        """
        mepo1 to mepo2 includes renaming of directories
        Since pickle requires that "the class definition must be importable
        and live in the same module as when the object was stored", we need to
        patch sys.modules to be able to read mepo1 state
        """
        import mepo

        sys.modules["state"] = mepo.state
        sys.modules["state.component"] = mepo.component
        sys.modules["utilities"] = mepo.utilities

    @staticmethod
    def mepo1_patch_undo():
        """
        Undo changes made my __mepo1_patch(). Called during <mepo update-state>
        """
        entries_to_remove = ["state", "state.component", "utilities"]
        for key in entries_to_remove:
            sys.modules.pop(key, None)

    @classmethod
    def read_state(cls):
        if cls.state_exists():
            with open(cls.get_file(), "r") as fin:
                allcomps_s = json.load(fin)
            # List of dicts -> state (list of MepoComponent objects)
            allcomps = []
            for comp_s in allcomps_s:
                comp = MepoComponent().deserialize(comp_s)
                # Relative path to absolute
                comp.local = os.path.join(cls.get_root_dir(), comp.local)
                allcomps.append(comp)
            return allcomps
        elif cls.state_exists(old_style=True):
            print(
                colors.YELLOW
                + "Detected mepo1 style state\n"
                + "Run <mepo update-state> to permanently convert to mepo2 style"
                + colors.RESET
            )
            cls.__mepo1_patch()
            with open(cls.get_file(old_style=True), "rb") as fin:
                allcomps = pickle.load(fin)
            for comp in allcomps:
                comp.local = os.path.join(cls.get_root_dir(), comp.local)
        else:
            raise StateDoesNotExistError("Error! mepo state does not exist")
        return allcomps

    @classmethod
    def __get_new_state_file(cls):
        """Return full path to the new state file to write to"""
        if cls.state_exists():
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), "state.*.json")
            states = [os.path.basename(x) for x in glob.glob(pattern)]
            new_state_id = max([int(x.split(".")[1]) for x in states]) + 1
            state_filename = "state." + str(new_state_id) + ".json"
        elif cls.state_exists(old_style=True):
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), "state.*.pkl")
            states = [os.path.basename(x) for x in glob.glob(pattern)]
            new_state_id = max([int(x.split(".")[1]) for x in states])
            state_filename = "state." + str(new_state_id) + ".json"
        else:
            state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
            os.makedirs(state_dir, exist_ok=True)
            state_filename = "state.0.json"
        return os.path.join(state_dir, state_filename)

    @classmethod
    def write_state(cls, allcomps):
        new_state_file = cls.__get_new_state_file()
        allcomps_s = []
        for comp in allcomps:
            # Save relative path (to fixture dir) to state
            comp.local = os.path.relpath(comp.local, start=cls.get_root_dir())
            allcomps_s.append(comp.serialize())
        with open(new_state_file, "w") as fout:
            json.dump(allcomps_s, fout)
        # Make the state file read-only
        os.chmod(new_state_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        # Update symlink
        state_dir = os.path.dirname(new_state_file)
        state_fileptr_fullpath = os.path.join(state_dir, cls.__state_fileptr_name)
        if os.path.isfile(state_fileptr_fullpath):
            os.remove(state_fileptr_fullpath)
        with mepo_chdir(state_dir):
            new_state_filename = os.path.basename(new_state_file)
            os.symlink(new_state_filename, cls.__state_fileptr_name)

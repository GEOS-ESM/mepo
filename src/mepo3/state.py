import os
import glob
import json
import stat

try:
    import contextlib.chdir as mepo_chdir
except:
    from .utilities.chdir import chdir as mepo_chdir

from .component import MepoComponent
from .utilities.exceptions import StateDoesNotExistError


class MepoState:

    __state_dir_name = ".mepo3"
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
        raise OSError("mepo3 state dir [.mepo3] does not exist")

    @classmethod
    def get_root_dir(cls):
        """Return fixture (root) directory that contains .mepo3"""
        return os.path.dirname(cls.get_dir())

    @classmethod
    def get_file(cls):
        """Return location of mepo state file"""
        state_file = os.path.join(cls.get_dir(), cls.__state_fileptr_name)
        if os.path.exists(state_file):
            return state_file
        raise OSError(f"mepo3 state file [{state_file}] does not exist")

    @classmethod
    def state_exists(cls):
        try:
            cls.get_file()
            return True
        except OSError:
            return False

    @classmethod
    def read_state(cls):
        if cls.state_exists():
            with open(cls.get_file(), "r") as fin:
                allcomps_s = json.load(fin)
            # List of dicts -> state (list of MepoComponent objects)
            allcomps = []
            for comp in allcomps_s:
                allcomps.append(MepoComponent().deserialize(comp))
            return allcomps
        else:
            raise StateDoesNotExistError("Error! mepo3 state does not exist")

    @classmethod
    def __get_new_state_file(cls):
        """Return full path to the new state file to write to"""
        if cls.state_exists():
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), "state.*.json")
            states = [os.path.basename(x) for x in glob.glob(os.path.join(pattern))]
            new_state_id = max([int(x.split(".")[1]) for x in states]) + 1
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

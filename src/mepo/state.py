import os
import sys
import yaml
import glob
import pickle

from pathlib import Path

from .registry import Registry
from .component import MepoComponent
from .utilities import shellcmd
from .utilities import colors
from .utilities.exceptions import StateDoesNotExistError
from .utilities.exceptions import StateAlreadyInitializedError

class MepoState(object):

    __state_dir_name = '.mepo'
    __state_fileptr_name = 'state.pkl'

    @staticmethod
    def get_parent_dirs():
        mypath = os.getcwd()
        parentdirs = [mypath]
        while mypath != '/':
            mypath = os.path.dirname(mypath)
            parentdirs.append(mypath)
        return parentdirs

    @classmethod
    def get_dir(cls):
        for mydir in cls.get_parent_dirs():
            state_dir = os.path.join(mydir, cls.__state_dir_name)
            if os.path.exists(state_dir):
                return state_dir
        raise OSError('mepo state dir [.mepo] does not exist')

    @classmethod
    def get_root_dir(cls):
        '''Return directory that contains .mepo'''
        return os.path.dirname(cls.get_dir())

    @classmethod
    def get_file(cls):
        state_file = os.path.join(cls.get_dir(), cls.__state_fileptr_name)
        if os.path.exists(state_file):
            return state_file
        raise OSError('mepo state file [%s] does not exist' % state_file)

    @classmethod
    def exists(cls):
        try:
            cls.get_file()
            return True
        except OSError:
            return False

    @classmethod
    def initialize(cls, project_registry, directory_style):
        if cls.exists():
            raise StateAlreadyInitializedError('Error! mepo state already exists')
        input_components = Registry(project_registry).read_file()

        num_fixture = 0
        complist = list()
        for name, comp in input_components.items():
            # We only allow one fixture
            if 'fixture' in comp:
                num_fixture += comp['fixture']
            if num_fixture > 1:
                raise Exception("Only one fixture allowed")

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
            + 'Converting mepo1 state to mepo2 state\n'
            + "Run <mepo update-state> to permanently convert to mepo2 state"
            + colors.RESET)
        import mepo
        sys.modules['state'] = mepo.state
        sys.modules['state.component'] = mepo.component
        sys.modules['utilities'] = mepo.utilities

    @staticmethod
    def mepo1_patch_undo():
        """
        Undo changes made my __mepo1_patch(). Called during <mepo update-state>
        """
        import mepo
        entries_to_remove = ['state', 'state.component', 'utilities']
        for key in entries_to_remove:
            sys.modules.pop(key, None)

    @classmethod
    def read_state(cls):
        if not cls.exists():
            raise StateDoesNotExistError('Error! mepo state does not exist')
        with open(cls.get_file(), 'rb') as fin:
            try:
                allcomps = pickle.load(fin)
            except ModuleNotFoundError:
                cls.__mepo1_patch()
                fin.seek(0)
                allcomps = pickle.load(fin)
        return allcomps

    @classmethod
    def write_state(cls, state_details):
        if cls.exists():
            state_dir = cls.get_dir()
            pattern = os.path.join(cls.get_dir(), 'state.*.pkl')
            states = [os.path.basename(x) for x in glob.glob(os.path.join(pattern))]
            new_state_id = max([int(x.split('.')[1]) for x in states]) + 1
            state_file_name = 'state.' + str(new_state_id) + '.pkl'
        else:
            state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
            os.mkdir(state_dir)
            state_file_name = 'state.0.pkl'
        new_state_file = os.path.join(state_dir, state_file_name)
        with open(new_state_file, 'wb') as fout:
            pickle.dump(state_details, fout, -1)
        state_fileptr = cls.__state_fileptr_name
        state_fileptr_fullpath = os.path.join(state_dir, state_fileptr)
        if os.path.isfile(state_fileptr_fullpath):
            os.remove(state_fileptr_fullpath)
        #os.symlink(new_state_file, state_fileptr_fullpath)
        curr_dir=os.getcwd()
        os.chdir(state_dir)
        os.symlink(state_file_name, state_fileptr)
        os.chdir(curr_dir)

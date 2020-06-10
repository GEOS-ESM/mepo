import os
import sys
import yaml
import glob
import pickle

from config.config_file import ConfigFile
from state.component import MepoComponent
from utilities import shellcmd
from pathlib import Path
from urllib.parse import urljoin
from utilities import colors
from utilities import meporc


class MepoStateDoesNotExistError(Exception):
    """Raised when the mepo state does not exist"""
    pass

class MepoStateAlreadyInitializedError(Exception):
    """Raised when the mepo state has already been initialized"""
    pass

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
    def initialize(cls, project_config_file, develop_from_argparse):
        if cls.exists():
            raise MepoStateAlreadyInitializedError('mepo state already exists')

        default_meporc_file = os.path.expanduser('~/.meporc')
        alternate_develop = None

        # Now we look for alternate develop branches
        # First if an argument was sent in...
        if develop_from_argparse:
            # An argparse nargs=1 provides a list
            alternate_develop = develop_from_argparse[0]
        # Then MEPORC wins...
        elif 'MEPORC' in os.environ:
            meporc_file = os.environ.get('MEPORC')
            if os.path.isfile(meporc_file):
                print("Found MEPORC in environment: [%s]" % meporc_file)
                meporc_dict = meporc.parse(meporc_file)
                if 'develop' in meporc_dict:
                    alternate_develop = meporc_dict['develop']
                else:
                    raise OSError('develop field not in [%s]' % meporc_file)
            else:
                raise FileNotFoundError('MEPORC in environment but file [%s] does not exist' % meporc_file)
        elif os.path.isfile(default_meporc_file):
            print("Found ~/.meporc")
            meporc_dict = meporc.parse(default_meporc_file)
            if 'develop' in meporc_dict:
                alternate_develop = meporc_dict['develop']
            else:
                raise OSError('develop field not in [%s]' % default_meporc_file)

        if alternate_develop is not None:
            new_develop_branch = colors.YELLOW + alternate_develop + colors.RESET
            print("Changing develop branch to: {new_develop_branch}".format(new_develop_branch=new_develop_branch))
        input_components = ConfigFile(project_config_file, alternate_develop).read_file()
        complist = list()
        for name, comp in input_components.items():
            for key, value in comp.items():
                if key == "remote":
                    if comp[key].startswith('..'):
                        rel_remote = os.path.basename(comp[key])
                        fixture_url = get_current_remote_url()
                        resolved_remote = urljoin(fixture_url,rel_remote)
                        comp[key] = resolved_remote
            complist.append(MepoComponent().to_component(name, comp))
        cls.write_state(complist)

    @classmethod
    def read_state(cls):
        if not cls.exists():
            raise MepoStateDoesNotExistError('mepo state does not exist')
        with open(cls.get_file(), 'rb') as fin:
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
        state_fileptr = os.path.join(state_dir, cls.__state_fileptr_name)
        if os.path.isfile(state_fileptr):
            os.remove(state_fileptr)
        os.symlink(new_state_file, state_fileptr)

def get_current_remote_url():
    cmd = 'git remote get-url origin'
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output

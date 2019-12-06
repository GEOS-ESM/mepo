import os
import sys
import yaml
import pickle

import utilities.path as utilspath
from config.config_file import ConfigFile

class MepoState(object):

    __state_dir_name = '.mepo'
    __state_0_file_name = 'state.0.pkl'
    __state_file_name = 'state.pkl'

    @classmethod
    def get_dir(cls):
        for mydir in utilspath.get_parent_dirs():
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
        state_file = os.path.join(cls.get_dir(), cls.__state_file_name)
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
    def initialize(cls, project_config_file):
        if cls.exists():
            raise Exception('mepo state already exists')
        repolist = ConfigFile(project_config_file).read_file()
        repolist_abspath = utilspath.relpath_to_abs(repolist)
        cls.write_state(repolist_abspath)

    @classmethod
    def read_state(cls):
        if not cls.exists():
            raise Exception('mepo state does not exist')
        with open(cls.get_file(), 'rb') as fin:
            allrepos = pickle.load(fin)
        return allrepos

    @classmethod
    def write_state(cls, state_details):
        new_state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
        os.mkdir(new_state_dir)
        new_state_file = os.path.join(new_state_dir, cls.__state_0_file_name)
        with open(new_state_file, 'wb') as fout:
            pickle.dump(state_details, fout, -1)
        state_file = os.path.join(cls.__state_dir_name, cls.__state_file_name)
        os.symlink(new_state_file, state_file)

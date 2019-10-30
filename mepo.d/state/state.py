import os
import sys
import csv
import json

import cPickle as pickle

from collections import OrderedDict

KEYLIST = ['level', 'name', 'origin', 'tag', 'branch', 'path']

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def flatten_nested_dict(nestedd, flatd=None, keywd='Components', level=0):
    if flatd is None:
        flatd = OrderedDict()
    for name, repo in nestedd[keywd].items():
        flatd[name] = OrderedDict([('level', level)])
        for key, value in repo.items():
            if key == keywd:
                flatten_nested_dict(repo, flatd, keywd, level+1) # recurse
            else:
                flatd[name][key] = value
    return flatd
            
def convert_relpath_to_abs(repolist, keywd='Components'):
    for name, repo in repolist[keywd].items():
        for key, value in repo.items():
            if key == keywd:
                convert_relpath_to_abs(repo)
            else:
                if key == 'local':
                    repo[key] = os.path.abspath(value)
    return repolist
                    
class MepoState(object):

    __state_dir_name = '.mepo'
    __state_0_file_name = 'state.0.pkl'
    __state_file_name = 'state.pkl'

    @classmethod
    def get_dir(cls):
        for mydir in get_parent_dirs():
            state_dir = os.path.join(mydir, cls.__state_dir_name)
            if os.path.exists(state_dir):
                return state_dir
        raise OSError('mepo state dir [.mepo] does not exist')

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
            sys.exit('ERROR: mepo state already exists')
        new_state_dir = os.path.join(os.getcwd(), cls.__state_dir_name)
        new_state_file = os.path.join(new_state_dir, cls.__state_0_file_name)
        os.mkdir(new_state_dir)
        with open(project_config_file, 'r') as fin:
            repolist = json.load(fin, object_pairs_hook=OrderedDict)
        repolist = convert_relpath_to_abs(repolist)
        repolist_flattened = flatten_nested_dict(repolist)
        with open(new_state_file, 'wb') as fout:
            pickle.dump(repolist_flattened, fout, -1)
        state_file = os.path.join(cls.__state_dir_name, cls.__state_file_name)
        os.symlink(new_state_file, state_file)
        return repolist_flattened
        
    @classmethod
    def read_state(cls):
        if not cls.exists():
            sys.exit('ERROR: mepo state does not exist')
        with open(cls.get_file(), 'rb') as fin:
            allrepos = pickle.load(fin)
        return allrepos

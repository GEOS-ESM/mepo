import os
import sys
import csv
import json

from collections import OrderedDict

KEYLIST = ['level', 'name', 'origin', 'tag', 'branch', 'path']

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def write_state(repolist, csv_writer, level=0):
    myrepos = repolist['Components']
    for reponame in myrepos:
        repo = myrepos[reponame]
        remote = repo['remote']
        branch = repo.get('branch') # d.get(key) is None if key is not present
        tag = repo.get('tag')
        # TODO: Can't have both branch and tag
        local_path = os.path.join(os.getcwd(), repo['local'])
        csv_writer.writerow([level, reponame, remote, tag, branch, local_path])
        if 'Components' in repo:
            write_state(repo, csv_writer, level+1) # recurse

class MepoState(object):

    __dirname = '.mepo'
    __filename = 'state.csv'

    @classmethod
    def get_dir(cls):
        for mydir in get_parent_dirs():
            mepo_dir = os.path.join(mydir, cls.__dirname)
            if os.path.exists(mepo_dir):
                return mepo_dir
        raise OSError('mepo dir [.mepo] does not exist')

    @classmethod
    def get_file(cls):
        mepo_file = os.path.join(cls.get_dir(), cls.__filename)
        if os.path.exists(mepo_file):
            return mepo_file
        raise OSError('mepo file [%s] does not exist' % mepo_file)

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
        new_mepo_dir = os.path.join(os.getcwd(), cls.__dirname)
        new_mepo_file = os.path.join(new_mepo_dir, cls.__filename)
        os.mkdir(new_mepo_dir)
        with open(project_config_file, 'r') as fin:
            repolist = json.load(fin, object_pairs_hook=OrderedDict)
        with open(new_mepo_file, 'w') as fout:
            csv_writer = csv.writer(fout, delimiter = ',', quotechar = '"')
            csv_writer.writerow(KEYLIST)
            write_state(repolist, csv_writer)
        
    @classmethod
    def read_state(cls):
        if not cls.exists():
            sys.exit('ERROR: mepo state does not exist')
        allrepos = OrderedDict()
        with open(cls.get_file(), 'r') as fin:
            reader = csv.DictReader(fin, delimiter = ',')
            for row in reader:
                reponame = row['name']
                allrepos[reponame] = dict()
                for key in KEYLIST:
                    if key != 'name':
                        allrepos[reponame].update({key: row[key]})
        return allrepos

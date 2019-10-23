# Initialize mepo

import os
import csv
import json

class MepoState(object):

    mepo_state_dir = os.path.join(os.getcwd(), '.mepo')
    mepo_state_file = os.path.join(mepo_state_dir, 'mepo-state.csv')
    
    @classmethod
    def exists(cls):
        if os.path.exists(cls.mepo_state_file):
            return True
        else:
            return False

    @classmethod
    def __somefunction(cls, repolist, csv_writer):
        myrepos = repolist['Components']
        for reponame in myrepos:
            repo = myrepos[reponame]
            origin = repo['url']
            branch = repo.get('branch') # d.get(key) is None if key not present
            tag = repo.get('tag')
            location = repo['local_path']
            csv_writer.writerow([reponame, origin, tag, branch, location])
            if 'Components' in repo:
                cls.__somefunction(repo, csv_writer) # recurse
            
    @classmethod
    def initialize(cls, project_config_file):
        if cls.exists():
            raise Exception("mepo state already exists")
        os.mkdir(cls.mepo_state_dir)
        with open(project_config_file, 'r') as fin:
            repolist = json.load(fin)
        with open(cls.mepo_state_file, 'w') as fout:
            csv_writer = csv.writer(fout, delimiter = ',', quotechar = '"')
            csv_writer.writerow(['name', 'origin', 'tag', 'branch', 'path'])
            cls.__somefunction(repolist, csv_writer)

    @classmethod
    def read_state(cls):
        if not cls.exists():
            raise Exception("mepo state does not exist")
        allrepos = []
        with open(cls.mepo_state_file, 'r') as fin:
            reader = csv.DictReader(fin, delimiter = ',')
            for row in reader:
                allrepos.append(row)
        return allrepos

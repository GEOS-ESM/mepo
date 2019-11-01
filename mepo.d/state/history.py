import os
import sys

class MepoHistory(object):

    __history_file_name = 'history'

    @classmethod
    def get_file(cls, mepo_dir):
        return os.path.join(mepo_dir, cls.__history_file_name)
    
    @classmethod
    def write_history(cls, mepo_dir):
        mepo_cmd = ['mepo'] + sys.argv[1:] + ['\n']
        with open(cls.get_file(mepo_dir), 'a') as fout:
            fout.write(' '.join(mepo_cmd))    

    @classmethod
    def read_history(cls, mepo_dir):
        with open(cls.get_file(mepo_dir), 'r') as fin:
            for line in fin:
                sys.stdout.write(line)

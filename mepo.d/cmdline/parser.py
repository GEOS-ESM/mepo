import argparse

from branch_parser import MepoBranchParser

class MepoParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description = 'Tool to manage (m)ultiple r(epo)s')
        self.subparsers = self.parser.add_subparsers(
            title = 'mepo commands',
            dest = 'mepo_cmd')

    def parse(self):
        self.__init()
        self.__clone()
        self.__status()
        self.__checkout()
        self.__branch()
        self.__diff()
        return self.parser.parse_args()
    
    def __init(self):
        init = self.subparsers.add_parser(
            'init',
            description = 'Initialize mepo')
        init.add_argument(
            '--config',
            metavar = 'config-file',
            default = 'repolist.json',
            help = 'default: %(default)s')

    def __clone(self):
        clone = self.subparsers.add_parser(
            'clone',
            description = 'Clone repos defined in config file')

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            description = 'Check status of all repos')
        
    def __checkout(self):
        checkout = self.subparsers.add_parser(
            'checkout',
            description = 'Switch to branch <branch-name> in repo <repo-name>')
        checkout.add_argument('branch_name', metavar = 'branch-name')
        checkout.add_argument('repo_name', metavar = 'repo-name', nargs = '+')

    def __branch(self):
        branch = self.subparsers.add_parser('branch')
        MepoBranchParser(branch)
        
    def __diff(self):
        diff = self.subparsers.add_parser(
            'diff',
            description = 'List difference between current and original states')

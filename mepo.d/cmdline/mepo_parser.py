import sys
import argparse

class MepoParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description = 'Tool to manage (m)ultiple r(epo)s')
        self.subparsers = self.parser.add_subparsers(
            title = 'mepo commands',
            dest = 'mepo_cmd')

    def parse(self):
        self.__clone()
        self.__status()
        self.__checkout()
        self.__branch()
        return self.parser.parse_args()
    
    def __clone(self):
        clone = self.subparsers.add_parser(
            'clone',
            description = 'Clone repos defined in config file')
        clone.add_argument(
            '--cf',
            metavar = 'config-file',
            default = 'repolist.json',
            help = 'default: %(default)s')

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
        branch = self.subparsers.add_parser(
            'branch',
            description = 'List branches in all repositories')
        branch.add_argument(
            '-a', '--all',
            action = 'store_true',
            help = 'list all (local & remote) branches')

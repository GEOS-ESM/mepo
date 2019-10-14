import sys
import argparse

from mepo_branch_parser import MepoBranchParser

class MepoParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description = 'Tool to manage (m)ultiple r(epo)s')
        self.subparsers = self.parser.add_subparsers(
            title='mepo commands',
            dest='mepo_cmd')

    def parse(self):
        self.__checkout()
        self.__status()
        self.__branch()
        return self.parser.parse_args()
    
    def __checkout(self):
        checkout = self.subparsers.add_parser(
            'checkout',
            help = 'checkout repos defined in config file')
        checkout.add_argument(
            '--config',
            default='repolist.yml',
            metavar = 'mepo-config-file')

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            help='run "git status" for each repo in config file')

    def __branch(self):
        branch = self.subparsers.add_parser(
            'branch',
            help = 'create, push or pull a branch in all repos')
        MepoBranchParser(branch)

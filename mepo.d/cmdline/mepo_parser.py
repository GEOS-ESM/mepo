import sys
import argparse

from mepo_branch_parser import MepoBranchParser

class MepoParser(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description = 'Tool to manage (m)ultiple r(epo)s')
        self.subparsers = self.parser.add_subparsers(
            title = 'mepo commands',
            dest = 'mepo_cmd')

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
            '--cf',
            metavar = 'config-file',
            default = 'repolist.json',
            help = 'default: %(default)s')

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            help = 'check status of all repos')
        
    def __branch(self):
        branch = self.subparsers.add_parser(
            'branch',
            help = 'run "mepo branch -h" for available sub-commands')
        MepoBranchParser(branch)

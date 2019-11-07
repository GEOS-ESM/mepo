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
        self.__compare()
        self.__where()
        self.__whereis()
        self.__history()
        self.__stage()
        return self.parser.parse_args()

    def __init(self):
        init = self.subparsers.add_parser(
            'init',
            description = 'Initialize mepo')
        init.add_argument(
            'config',
            metavar = 'config-file',
            nargs = '?',
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

    def __compare(self):
        compare = self.subparsers.add_parser(
            'compare',
            description = 'Compare current and original states')

    def __where(self):
        where = self.subparsers.add_parser(
            'where',
            description = 'Where am I w.r.t. other repos')

    def __whereis(self):
        whereis = self.subparsers.add_parser(
            'whereis',
            description = 'Get the location of repo <repo-name>')
        whereis.add_argument('repo_name', metavar = 'repo-name')

    def __history(self):
        history = self.subparsers.add_parser(
            'history',
            description = 'Get a history of mepo commands that were run')

    def __stage(self):
        stage = self.subparsers.add_parser(
            'stage',
            description = 'Stage files for committing. '
            'If a repo is specified, files are staged only in that repo.')
        stage.add_argument(
            'repo',
            nargs = '*',
            default = None
        )

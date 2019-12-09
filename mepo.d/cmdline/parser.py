import argparse

from cmdline.branch_parser import MepoBranchArgParser

class MepoArgParser(object):

    __slots__ = ['parser', 'subparsers']

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description = 'Tool to manage (m)ultiple r(epo)s')
        self.subparsers = self.parser.add_subparsers()
        self.subparsers.title = 'mepo commands'
        self.subparsers.required = True
        self.subparsers.dest = 'mepo_cmd'

    def parse(self):
        self.__init()
        self.__clone()
        self.__list()
        self.__status()
        self.__checkout()
        self.__branch()
        self.__develop()
        self.__compare()
        self.__whereis()
        self.__stage()
        self.__unstage()
        self.__commit()
        self.__push()
        self.__save()
        return self.parser.parse_args()

    def __init(self):
        init = self.subparsers.add_parser(
            'init',
            description = 'Initialize mepo based on <config-file')
        init.add_argument(
            'config_file',
            metavar = 'config-file',
            nargs = '?',
            default = 'repolist.yaml',
            help = 'default: %(default)s')

    def __clone(self):
        clone = self.subparsers.add_parser(
            'clone',
            description = 'Clone repositories defined in config file')

    def __list(self):
        listrepos = self.subparsers.add_parser(
            'list',
            description = 'List all repositories that are being tracked')

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            description = 'Check current status of all repositories')

    def __checkout(self):
        checkout = self.subparsers.add_parser(
            'checkout',
            description = 'Switch to branch <branch-name> in repo <repo-name>. '
            'Specifying -b causes the branch <branch-name> to be created in '
            'the specified repos')
        checkout.add_argument('branch_name', metavar = 'branch-name')
        checkout.add_argument('repo_name', metavar = 'repo-name', nargs = '+')
        checkout.add_argument('-b', action = 'store_true', help = 'create the branch')

    def __branch(self):
        branch = self.subparsers.add_parser('branch')
        MepoBranchArgParser(branch)

    def __develop(self):
        develop = self.subparsers.add_parser(
            'develop',
            description = "Checkout current version of 'develop' branches of specified repos")
        develop.add_argument('repo_name', metavar = 'repo-name', nargs = '+', default = None)
        
    def __compare(self):
        compare = self.subparsers.add_parser(
            'compare',
            description = 'Compare current and original states of all repositories')

    def __whereis(self):
        whereis = self.subparsers.add_parser(
            'whereis',
            description = 'Get the location of repository <repo-name> '
            'relative to my current location. If <repo-name> is not present, '
            'get the relative locations of all repositories.')
        whereis.add_argument('repo_name', metavar = 'repo-name', nargs = '?', default = None)

    def __stage(self):
        stage = self.subparsers.add_parser(
            'stage',
            description = 'Stage modified & untracked files in the specified repo(s)')
        stage.add_argument(
            'repo_name',
            metavar = 'repo-name',
            nargs = '+',
            help = 'Repository to stage file in')

    def __unstage(self):
        unstage = self.subparsers.add_parser(
            'unstage',
            description = 'Un-stage staged files. '
            'If a repository is specified, files are un-staged only in that repository.')
        unstage.add_argument(
            'repo_name',
            metavar = 'repo-name',
            nargs = '*',
            help = 'Repository',
            default = None)

    def __commit(self):
        commit = self.subparsers.add_parser(
            'commit',
            description = 'Commit staged files in the specified repositories')
        commit.add_argument('message', metavar = 'message')
        commit.add_argument(
            'repo_name',
            metavar = 'repo-name',
            nargs = '+',
            help = 'Repository to stage file in')

    def __push(self):
        push = self.subparsers.add_parser(
            'push',
            description = 'Push local commits to remote')
        push.add_argument(
            'repo_name',
            metavar = 'repo-name',
            nargs = '+',
            help = 'Repository to stage file in')

    def __save(self):
        save = self.subparsers.add_parser(
            'save',
            description = 'Save current state in a yaml config file')
        save.add_argument(
            'config_file',
            metavar = 'config-file',
            nargs = '?',
            default = 'repolist-new.yaml',
            help = 'default: %(default)s')

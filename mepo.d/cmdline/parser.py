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
            description = 'Initialize mepo based on <config-file>')
        init.add_argument(
            'config_file',
            metavar = 'config-file',
            nargs = '?',
            default = 'components.yaml',
            help = 'default: %(default)s')

    def __clone(self):
        clone = self.subparsers.add_parser(
            'clone',
            description = "Clone repositories. Command 'mepo init' should have already been run")

    def __list(self):
        listcomps = self.subparsers.add_parser(
            'list',
            description = 'List all components that are being tracked')

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            description = 'Check current status of all components')

    def __checkout(self):
        checkout = self.subparsers.add_parser(
            'checkout',
            description = 'Switch to branch <branch-name> in component <comp-name>. '
            'Specifying -b causes the branch <branch-name> to be created in '
            'the specified component(s).')
        checkout.add_argument('branch_name', metavar = 'branch-name')
        checkout.add_argument('comp_name', metavar = 'comp-name', nargs = '+')
        checkout.add_argument('-b', action = 'store_true', help = 'create the branch')

    def __branch(self):
        branch = self.subparsers.add_parser('branch')
        MepoBranchArgParser(branch)

    def __develop(self):
        develop = self.subparsers.add_parser(
            'develop',
            description = "Checkout current version of 'develop' branches of specified components")
        develop.add_argument('comp_name', metavar = 'comp-name', nargs = '+', default = None)
        
    def __compare(self):
        compare = self.subparsers.add_parser(
            'compare',
            description = 'Compare current and original states of all components')

    def __whereis(self):
        whereis = self.subparsers.add_parser(
            'whereis',
            description = 'Get the location of component <comp-name> '
            'relative to my current location. If <comp-name> is not present, '
            'get the relative locations of ALL components.')
        whereis.add_argument('comp_name', metavar = 'comp-name', nargs = '?', default = None)

    def __stage(self):
        stage = self.subparsers.add_parser(
            'stage',
            description = 'Stage modified & untracked files in the specified component(s)')
        stage.add_argument(
            '--untracked',
            action = 'store_true',
            help = 'stage untracked files as well')
        stage.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to stage file in')

    def __unstage(self):
        unstage = self.subparsers.add_parser(
            'unstage',
            description = 'Un-stage staged files. '
            'If a component is specified, files are un-staged only for that component.')
        unstage.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '*',
            help = 'Component',
            default = None)

    def __commit(self):
        commit = self.subparsers.add_parser(
            'commit',
            description = 'Commit staged files in the specified components')
        commit.add_argument('message', metavar = 'message')
        commit.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to stage file in')

    def __push(self):
        push = self.subparsers.add_parser(
            'push',
            description = 'Push local commits to remote')
        push.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to push to remote')

    def __save(self):
        save = self.subparsers.add_parser(
            'save',
            description = 'Save current state in a yaml config file')
        save.add_argument(
            'config_file',
            metavar = 'config-file',
            nargs = '?',
            default = 'components-new.yaml',
            help = 'default: %(default)s')

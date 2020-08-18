import argparse

from cmdline.branch_parser import MepoBranchArgParser
from cmdline.stash_parser  import MepoStashArgParser

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
        self.__restore_state()
        self.__diff()
        self.__fetch()
        self.__fetch_all()
        self.__checkout()
        self.__checkout_if_exists()
        self.__branch()
        self.__stash()
        self.__develop()
        self.__pull()
        self.__pull_all()
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
            '--config',
            metavar = 'config-file',
            nargs = '?',
            default = 'components.yaml',
            help = 'default: %(default)s')

    def __clone(self):
        clone = self.subparsers.add_parser(
            'clone',
            description = "Clone repositories.")
        clone.add_argument(
            'repo_url',
            metavar = 'URL',
            nargs = '?',
            default = None,
            help = 'URL to clone')
        clone.add_argument(
            'directory',
            nargs = '?',
            default = None,
            help = "Directory to clone into (Only allowed with URL!)")
        clone.add_argument(
            '--branch','-b',
            metavar = 'name',
            nargs = '?',
            default = None,
            help = 'Branch/tag of URL to initially clone (Only allowed with URL!)')
        clone.add_argument(
            '--config',
            metavar = 'config-file',
            nargs = '?',
            default = 'components.yaml',
            help = 'Configuration file (ignored if init already called, default: %(default)s)')

    def __list(self):
        listcomps = self.subparsers.add_parser(
            'list',
            description = 'List all components that are being tracked')

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            description = 'Check current status of all components')

    def __restore_state(self):
        restore_state = self.subparsers.add_parser(
            'restore-state',
            description = 'Restores all components to the last saved state.')

    def __diff(self):
        diff = self.subparsers.add_parser(
            'diff',
            description = 'Diff all components')
        diff.add_argument('--name-only', action = 'store_true', help = 'Show only names of changed files')

    def __checkout(self):
        checkout = self.subparsers.add_parser(
            'checkout',
            description = 'Switch to branch <branch-name> in component <comp-name>. '
            'Specifying -b causes the branch <branch-name> to be created in '
            'the specified component(s).')
        checkout.add_argument('branch_name', metavar = 'branch-name')
        checkout.add_argument('comp_name', metavar = 'comp-name', nargs = '+')
        checkout.add_argument('-b', action = 'store_true', help = 'create the branch')

    def __checkout_if_exists(self):
        checkout_if_exists = self.subparsers.add_parser(
            'checkout-if-exists',
            description = 'Switch to branch <branch-name> in any component where it is present. ')
        checkout_if_exists.add_argument('branch_name', metavar = 'branch-name')
        checkout_if_exists.add_argument('--quiet', action = 'store_true', help = 'Suppress found messages')

    def __fetch(self):
        fetch = self.subparsers.add_parser(
            'fetch',
            description = 'Download objects and refs from in component <comp-name>. '
            'Specifying --all causes all remotes to be fetched.')
        fetch.add_argument('comp_name', metavar = 'comp-name', nargs = '+')
        fetch.add_argument('--all', action = 'store_true', help = 'Fetch all remotes.')
        fetch.add_argument('--prune','-p', action = 'store_true', help = 'Prune remote branches.')
        fetch.add_argument('--tags','-t', action = 'store_true', help = 'Fetch tags.')

    def __fetch_all(self):
        fetch_all = self.subparsers.add_parser(
            'fetch-all',
            description = 'Download objects and refs from all components. '
            'Specifying --all causes all remotes to be fetched.')
        fetch_all.add_argument('--all', action = 'store_true', help = 'Fetch all remotes.')
        fetch_all.add_argument('--prune','-p', action = 'store_true', help = 'Prune remote branches.')
        fetch_all.add_argument('--tags','-t', action = 'store_true', help = 'Fetch tags.')

    def __branch(self):
        branch = self.subparsers.add_parser('branch')
        MepoBranchArgParser(branch)

    def __stash(self):
        stash = self.subparsers.add_parser(
                'stash',
                description = "Runs stash commands.")
        MepoStashArgParser(stash)

    def __develop(self):
        develop = self.subparsers.add_parser(
            'develop',
            description = "Checkout current version of 'develop' branches of specified components")
        develop.add_argument('comp_name', metavar = 'comp-name', nargs = '+', default = None)

    def __pull(self):
        pull = self.subparsers.add_parser(
            'pull',
            description = "Pull branches of specified components")
        pull.add_argument('comp_name', metavar = 'comp-name', nargs = '+', default = None)

    def __pull_all(self):
        pull_all = self.subparsers.add_parser(
            'pull-all',
            description = "Pull branches of all components (only those in non-detached HEAD state)")

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
        commit.add_argument('-m', '--message', type=str, metavar = 'message', default=None)
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

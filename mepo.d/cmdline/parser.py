import argparse

from cmdline.branch_parser import MepoBranchArgParser
from cmdline.stash_parser  import MepoStashArgParser
from cmdline.tag_parser    import MepoTagArgParser
from cmdline.config_parser import MepoConfigArgParser
from cmdline.patch_parser  import MepoPatchArgParser
from utilities             import mepoconfig

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
        self.__tag()
        self.__stash()
        self.__patch()
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
        self.__config()
        return self.parser.parse_args()

    def __init(self):
        init = self.subparsers.add_parser(
            'init',
            description = 'Initialize mepo based on <config-file>',
            aliases=mepoconfig.get_command_alias('init'))
        init.add_argument(
            '--config',
            metavar = 'config-file',
            nargs = '?',
            default = 'components.yaml',
            help = 'default: %(default)s')
        init.add_argument(
            '--style',
            metavar = 'style-type',
            nargs = '?',
            default = None,
            choices = ['naked', 'prefix','postfix'],
            help = 'Style of directory file, default: prefix, allowed options: %(choices)s')

    def __clone(self):
        clone = self.subparsers.add_parser(
            'clone',
            description = "Clone repositories.",
            aliases=mepoconfig.get_command_alias('clone'))
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
            default = None,
            help = 'Configuration file (ignored if init already called)')
        clone.add_argument(
            '--style',
            metavar = 'style-type',
            nargs = '?',
            default = None,
            choices = ['naked', 'prefix','postfix'],
            help = 'Style of directory file, default: prefix, allowed options: %(choices)s (ignored if init already called)')

    def __list(self):
        listcomps = self.subparsers.add_parser(
            'list',
            description = 'List all components that are being tracked',
            aliases=mepoconfig.get_command_alias('list'))

    def __status(self):
        status = self.subparsers.add_parser(
            'status',
            description = 'Check current status of all components',
            aliases=mepoconfig.get_command_alias('status'))

    def __restore_state(self):
        restore_state = self.subparsers.add_parser(
            'restore-state',
            description = 'Restores all components to the last saved state.',
            aliases=mepoconfig.get_command_alias('restore-state'))

    def __diff(self):
        diff = self.subparsers.add_parser(
            'diff',
            description = 'Diff all components',
            aliases=mepoconfig.get_command_alias('diff'))
        diff.add_argument(
            '--name-only',
            action = 'store_true',
            help = 'Show only names of changed files')
        diff.add_argument(
            '--staged',
            action = 'store_true',
            help = 'Show diff of staged changes')
        diff.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '*',
            help = 'Component to list branches in')

    def __checkout(self):
        checkout = self.subparsers.add_parser(
            'checkout',
            description = 'Switch to branch <branch-name> in component <comp-name>. '
            'Specifying -b causes the branch <branch-name> to be created in '
            'the specified component(s).',
            aliases=mepoconfig.get_command_alias('checkout'))
        checkout.add_argument('branch_name', metavar = 'branch-name')
        checkout.add_argument('comp_name', metavar = 'comp-name', nargs = '+')
        checkout.add_argument('-b', action = 'store_true', help = 'create the branch')
        checkout.add_argument('--quiet', '-q', action = 'store_true', help = 'Suppress prints')

    def __checkout_if_exists(self):
        checkout_if_exists = self.subparsers.add_parser(
            'checkout-if-exists',
            description = 'Switch to branch <branch-name> in any component where it is present. ',
            aliases=mepoconfig.get_command_alias('checkout-if-exists'))
        checkout_if_exists.add_argument('branch_name', metavar = 'branch-name')
        checkout_if_exists.add_argument('--quiet', '-q', action = 'store_true', help = 'Suppress prints')
        checkout_if_exists.add_argument('--dry-run','-n', action = 'store_true', help = 'Dry-run only (lists repos where branch exists)')

    def __fetch(self):
        fetch = self.subparsers.add_parser(
            'fetch',
            description = 'Download objects and refs from in component <comp-name>. '
            'Specifying --all causes all remotes to be fetched.',
            aliases=mepoconfig.get_command_alias('fetch'))
        fetch.add_argument('comp_name', metavar = 'comp-name', nargs = '+')
        fetch.add_argument('--all', action = 'store_true', help = 'Fetch all remotes.')
        fetch.add_argument('--prune','-p', action = 'store_true', help = 'Prune remote branches.')
        fetch.add_argument('--tags','-t', action = 'store_true', help = 'Fetch tags.')
        fetch.add_argument('--force','-f', action = 'store_true', help = 'Force action.')

    def __fetch_all(self):
        fetch_all = self.subparsers.add_parser(
            'fetch-all',
            description = 'Download objects and refs from all components. '
            'Specifying --all causes all remotes to be fetched.',
            aliases=mepoconfig.get_command_alias('fetch-all'))
        fetch_all.add_argument('--all', action = 'store_true', help = 'Fetch all remotes.')
        fetch_all.add_argument('--prune','-p', action = 'store_true', help = 'Prune remote branches.')
        fetch_all.add_argument('--tags','-t', action = 'store_true', help = 'Fetch tags.')
        fetch_all.add_argument('--force','-f', action = 'store_true', help = 'Force action.')

    def __branch(self):
        branch = self.subparsers.add_parser(
            'branch',
            description = "Runs branch commands.",
            aliases=mepoconfig.get_command_alias('branch'))
        MepoBranchArgParser(branch)

    def __stash(self):
        stash = self.subparsers.add_parser(
            'stash',
            description = "Runs stash commands.",
            aliases=mepoconfig.get_command_alias('stash'))
        MepoStashArgParser(stash)

    def __patch(self):
        patch = self.subparsers.add_parser(
            'patch',
            description = "Runs patch commands.")
        MepoPatchArgParser(patch)

    def __tag(self):
        tag = self.subparsers.add_parser(
            'tag',
            description = "Runs tag commands.",
            aliases=mepoconfig.get_command_alias('tag'))
        MepoTagArgParser(tag)

    def __develop(self):
        develop = self.subparsers.add_parser(
            'develop',
            description = "Checkout current version of 'develop' branches of specified components",
            aliases=mepoconfig.get_command_alias('develop'))
        develop.add_argument('comp_name', metavar = 'comp-name', nargs = '+', default = None)
        develop.add_argument('--quiet', '-q', action = 'store_true', help = 'Suppress prints')

    def __pull(self):
        pull = self.subparsers.add_parser(
            'pull',
            description = "Pull branches of specified components",
            aliases=mepoconfig.get_command_alias('pull'))
        pull.add_argument('comp_name', metavar = 'comp-name', nargs = '+', default = None)

    def __pull_all(self):
        pull_all = self.subparsers.add_parser(
            'pull-all',
            description = "Pull branches of all components (only those in non-detached HEAD state)",
            aliases=mepoconfig.get_command_alias('pull-all'))

    def __compare(self):
        compare = self.subparsers.add_parser(
            'compare',
            description = 'Compare current and original states of all components',
            aliases=mepoconfig.get_command_alias('compare'))

    def __whereis(self):
        whereis = self.subparsers.add_parser(
            'whereis',
            description = 'Get the location of component <comp-name> '
            'relative to my current location. If <comp-name> is not present, '
            'get the relative locations of ALL components.',
            aliases=mepoconfig.get_command_alias('whereis'))
        whereis.add_argument('comp_name', metavar = 'comp-name', nargs = '?', default = None)

    def __stage(self):
        stage = self.subparsers.add_parser(
            'stage',
            description = 'Stage modified & untracked files in the specified component(s)',
            aliases=mepoconfig.get_command_alias('stage'))
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
            'If a component is specified, files are un-staged only for that component.',
            aliases=mepoconfig.get_command_alias('unstage'))
        unstage.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '*',
            help = 'Component',
            default = None)

    def __commit(self):
        commit = self.subparsers.add_parser(
            'commit',
            description = 'Commit staged files in the specified components',
            aliases=mepoconfig.get_command_alias('commit'))
        commit.add_argument('-a', '--all', action = 'store_true', help = 'stage all tracked files and then commit')
        commit.add_argument('-m', '--message', type=str, metavar = 'message', default=None)
        commit.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to stage file in')

    def __push(self):
        push = self.subparsers.add_parser(
            'push',
            description = 'Push local commits or tags to remote',
            aliases=mepoconfig.get_command_alias('push'))
        push.add_argument(
            '--tags',
            action = 'store_true',
            help = 'push tags')
        push.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to push to remote')

    def __save(self):
        save = self.subparsers.add_parser(
            'save',
            description = 'Save current state in a yaml config file',
            aliases=mepoconfig.get_command_alias('save'))
        save.add_argument(
            'config_file',
            metavar = 'config-file',
            nargs = '?',
            default = 'components-new.yaml',
            help = 'default: %(default)s')

    def __config(self):
        config = self.subparsers.add_parser(
            'config',
            description = "Runs config commands.",
            aliases=mepoconfig.get_command_alias('config'))
        MepoConfigArgParser(config)

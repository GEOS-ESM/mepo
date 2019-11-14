import argparse

class MepoBranchArgParser(object):

    def __init__(self, branch):
        self.branch_subparsers = branch.add_subparsers()
        self.branch_subparsers.title = 'mepo branch sub-commands'
        self.branch_subparsers.dest = 'mepo_branch_cmd'
        self.branch_subparsers.required = True
        self.__list()
        self.__create()
        self.__delete()
        
    def __list(self):
        brlist = self.branch_subparsers.add_parser(
            'list',
            description = 'List local branches of all repos')
        brlist.add_argument(
            '-a', '--all',
            action = 'store_true',
            help = 'list all (local+remote) branches of all repos')

    def __create(self):
        create = self.branch_subparsers.add_parser(
            'create',
            description = 'Create branch <branch-name> in repo <repo-name>')
        create.add_argument('branch_name', metavar = 'branch-name')
        create.add_argument(
            'repo_name',
            metavar = 'repo-name',
            nargs = '+',
            help = 'Repo(s) to create branches in')

    def __delete(self):
        delete = self.branch_subparsers.add_parser(
            'delete',
            description = 'Delete branch <branch-name> in repo <repo-name>')
        delete.add_argument('branch_name', metavar = 'branch-name')
        delete.add_argument(
            'repo_name',
            metavar = 'repo-name',
            nargs = '+',
            help = 'Repo(s) to delete branches in')


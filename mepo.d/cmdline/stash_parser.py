import argparse

class MepoStashArgParser(object):

    def __init__(self, stash):
        self.stash = stash.add_subparsers()
        self.stash.title = 'mepo stash sub-commands'
        self.stash.dest = 'mepo_stash_cmd'
        self.stash.required = True
        self.__list()
        self.__pop()
        self.__apply()
        
    def __list(self):
        stlist = self.stash.add_parser(
            'list',
            description = 'List local stashes of all components')

    def __pop(self):
        stpop = self.stash.add_parser(
            'pop',
            description = 'Pop stash in component <comp-name>')
        stpop.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to pop stash in')

    def __apply(self):
        stapply = self.stash.add_parser(
            'apply',
            description = 'apply stash in component <comp-name>')
        stapply.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to apply stash in')

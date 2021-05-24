import argparse
import textwrap

class MepoConfigArgParser(object):

    def __init__(self, config):
        self.config = config.add_subparsers()
        self.config.title = 'mepo config sub-commands'
        self.config.dest = 'mepo_config_cmd'
        self.config.required = True
        self.__get()
        self.__set()
        self.__delete()
        self.__print()

    def __get(self):
        get = self.config.add_parser(
            'get',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                Get config <entry> in .mepoconfig.

                Note this uses gitconfig style where <entry> is
                of the form "section.option" So to get something like:

                    [alias]
                    st = status

                You would run "mepo config get alias.st"
                '''))
        get.add_argument(
            'entry',
            metavar = 'entry',
            help = 'Entry to display.')

    def __set(self):
        set = self.config.add_parser(
            'set',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                Set config <entry> to <value> in .mepoconfig.

                Note this uses gitconfig style where <entry> is
                of the form "section.option" So to set something like:

                    [alias]
                    st = status

                You would run "mepo config set alias.st status"
                '''))
        set.add_argument(
            'entry',
            metavar = 'entry',
            help = 'Entry to set.')
        set.add_argument(
            'value',
            metavar = 'value',
            help = 'Value to set entry to.')

    def __delete(self):
        delete = self.config.add_parser(
            'delete',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description = textwrap.dedent('''\
                Delete config <entry> in .mepoconfig.

                Note this uses gitconfig style where <entry> is
                of the form "section.option" So to delete something like:

                    [alias]
                    st = status

                You would run "mepo config delete alias.st"
                '''))
        delete.add_argument(
            'entry',
            metavar = 'entry',
            help = 'Entry to delete.')

    def __print(self):
        print = self.config.add_parser(
            'print',
            description = 'Print contents of .mepoconfig')

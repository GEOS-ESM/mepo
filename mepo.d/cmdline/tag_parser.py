import argparse

class MepoTagArgParser(object):

    def __init__(self, tag):
        self.tag = tag.add_subparsers()
        self.tag.title = 'mepo tag sub-commands'
        self.tag.dest = 'mepo_tag_cmd'
        self.tag.required = True
        self.__list()
        self.__create()
        self.__delete()
        
    def __list(self):
        tglist = self.tag.add_parser(
            'list',
            description = 'List tags.'
            'If no component is specified, runs over all components')
        tglist.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '*',
            help = 'Component to list tags in')

    def __create(self):
        create = self.tag.add_parser(
            'create',
            description = 'Create tag <tag-name> in component <comp-name>')
        create.add_argument('tag_name', metavar = 'tag-name')
        create.add_argument(
            '-a', '--annotate',
            action = 'store_true',
            help = "Make an annotated tag")
        create.add_argument(
            '-m', '--message',
            type=str,
            metavar = 'message',
            default = None,
            help = "Message for the tag"
            )
        create.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to create tags in')

    def __delete(self):
        delete = self.tag.add_parser(
            'delete',
            description = 'Delete tag <tag-name> in component <comp-name>')
        delete.add_argument('tag_name', metavar = 'tag-name')
        delete.add_argument(
            'comp_name',
            metavar = 'comp-name',
            nargs = '+',
            help = 'Component to delete tags in')

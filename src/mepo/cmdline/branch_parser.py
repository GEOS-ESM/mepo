class MepoBranchArgParser:

    def __init__(self, branch):
        self.branch_subparsers = branch.add_subparsers()
        self.branch_subparsers.title = "mepo branch sub-commands"
        self.branch_subparsers.dest = "mepo_branch_cmd"
        self.branch_subparsers.required = True
        self.__list()
        self.__create()
        self.__delete()

    def __list(self):
        brlist = self.branch_subparsers.add_parser(
            "list",
            description="List local branches. If no component is specified, runs over all components",
        )
        brlist.add_argument(
            "-a", "--all", action="store_true", help="list all (local+remote) branches"
        )
        brlist.add_argument(
            "--nocolor", action="store_true", help="do not display color"
        )
        brlist.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="*",
            help="component to list branches in",
        )

    def __create(self):
        create = self.branch_subparsers.add_parser(
            "create", description="Create branch <branch-name> in component <comp-name>"
        )
        create.add_argument("branch_name", metavar="branch-name", help="name of branch")
        create.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            help="component to create branches in",
        )

    def __delete(self):
        delete = self.branch_subparsers.add_parser(
            "delete", description="Delete branch <branch-name> in component <comp-name>"
        )
        delete.add_argument("branch_name", metavar="branch-name", help="name of branch")
        delete.add_argument(
            "comp_name",
            metavar="comp-name",
            nargs="+",
            help="component to delete branches in",
        )
        delete.add_argument(
            "--force",
            action="store_true",
            help="delete branch even if it has not been fully merged",
        )

from .branch_list import run as branch_list_run
from .branch_create import run as branch_create_run
from .branch_delete import run as branch_delete_run


def run(args):
    d = {
        "list": branch_list_run,
        "create": branch_create_run,
        "delete": branch_delete_run,
    }
    d[args.mepo_branch_cmd](args)

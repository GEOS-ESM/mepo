from .tag_list import run as tag_list_run
from .tag_create import run as tag_create_run
from .tag_delete import run as tag_delete_run
from .tag_push import run as tag_push_run


def run(args):
    d = {
        "list": tag_list_run,
        "create": tag_create_run,
        "delete": tag_delete_run,
        "push": tag_push_run,
    }
    d[args.mepo_tag_cmd](args)

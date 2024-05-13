from .config_get import run as config_get_run
from .config_set import run as config_set_run
from .config_delete import run as config_delete_run
from .config_print import run as config_print_run


def run(args):
    d = {
        "get": config_get_run,
        "set": config_set_run,
        "delete": config_delete_run,
        "print": config_print_run,
    }
    d[args.mepo_config_cmd](args)

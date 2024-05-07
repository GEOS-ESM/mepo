from .stash_list import run as stash_list_run
from .stash_pop import run as stash_pop_run
from .stash_apply import run as stash_apply_run
from .stash_push import run as stash_push_run
from .stash_show import run as stash_show_run


def run(args):
    d = {
        "list": stash_list_run,
        "pop": stash_pop_run,
        "apply": stash_apply_run,
        "push": stash_push_run,
        "show": stash_show_run,
    }
    d[args.mepo_stash_cmd](args)

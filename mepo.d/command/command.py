import os
import glob
from importlib import import_module

THIS_DIR = os.path.dirname(__file__)

def get_exclude_list():
    patterns = ['command.py', '*~', '__pycache__']
    exclude_list = list()
    for pat in patterns:
        tmp = glob.glob(os.path.join(THIS_DIR, pat))
        exclude_list.extend([os.path.basename(x) for x in tmp])
    return exclude_list

def get_available_mepo_commands():
    exclude_list = get_exclude_list()
    return [x for x in os.listdir(THIS_DIR) if x not in exclude_list]

def run(args):
    # Dispatch table: d = {'list': <module 'command.list.list'>, ...}
    cmd_list = get_available_mepo_commands()
    d = {x: import_module('command.{}.{}'.format(x, x)) for x in cmd_list}

    # Execute run method of specified mepo command, e.g. d['list'].run(args)
    d[args.mepo_cmd].run(args)

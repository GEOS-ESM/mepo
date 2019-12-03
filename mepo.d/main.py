import os
from importlib import import_module

from cmdline.parser import MepoArgParser

def get_available_mepo_commands():
    this_dir = os.path.dirname(__file__)
    cmd_dir = os.path.join(this_dir, 'command')
    excluded = ['__pycache__']
    return [name for name in os.listdir(cmd_dir) if name not in excluded]

def main():
    args = MepoArgParser().parse()

    # Dispatch table: d = {'list': <module 'command.list.list'>, ...}
    cmd_list = get_available_mepo_commands()
    d = {cmd: import_module('command.{}.{}'.format(cmd, cmd)) for cmd in cmd_list}
    
    # Execute run method of specified mepo command
    d[args.mepo_cmd].run(args)

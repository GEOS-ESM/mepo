from importlib import import_module

def run(args):
    mepo_cmd = args.mepo_cmd

    # Load the module containing the 'run' method of specified mepo command
    cmd_module = import_module('command.{}.{}'.format(mepo_cmd, mepo_cmd))

    # Execute 'run' method of the specified mepo command
    cmd_module.run(args)

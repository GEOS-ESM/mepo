from importlib import import_module

from ..utilities import mepoconfig

def run(args):
    mepo_cmd = mepoconfig.get_alias_command(args.mepo_cmd)

    # Load the module containing the 'run' method of specified mepo command
    cmd_module = import_module(f"mepo3.command.{mepo_cmd}")

    # Execute 'run' method of the specified mepo command
    cmd_module.run(args)

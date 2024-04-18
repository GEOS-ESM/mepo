"""
Provides a CLI for mepo. __main__.py is executed when the package mepo is
invoked directly via

> python -m mepo
"""

from importlib import import_module

from .cmdline.parser import MepoArgParser
from .utilities import mepoconfig


def main():
    """Parse command line options and execute the specified mepo command"""
    args = MepoArgParser().parse()
    mepo_cmd = mepoconfig.get_alias_command(args.mepo_cmd)

    # Load the module containing the "run" method of specified command
    cmd_module = import_module(f"mepo3.command.{mepo_cmd}")

    # Execute "run" method of specified command
    cmd_module.run(args)


if __name__ == "__main__":
    main()

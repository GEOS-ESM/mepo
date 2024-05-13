from importlib import import_module

from mepo.cmdline.parser import MepoArgParser
from mepo.utilities import mepoconfig


def main():
    args = MepoArgParser().parse()
    mepo_cmd = mepoconfig.get_alias_command(args.mepo_cmd)

    # Load the module containing the "run" method of specified command
    cmd_module = import_module(f"mepo.command.{mepo_cmd}")

    # Execute "run" method of specified command
    cmd_module.run(args)


if __name__ == "__main__":
    main()

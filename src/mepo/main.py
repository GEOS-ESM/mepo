from .cmdline.parser import MepoArgParser
from .command import command

def main():
    args = MepoArgParser().parse()
    command.run(args)

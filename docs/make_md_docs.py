#!/usr/bin/env python3

import os
import glob
import sys
from mdutils.mdutils import MdUtils
import subprocess as sp

preamble = """
mepo provides many different commands for working with a multi-repository fixture.

This reference is generated from the development source, including unreleased
changes. Run `mepo <command> --help` for the options in your installed version.
See [Configuration](Configuration) for released and unreleased retry settings.
"""

doc_dir_path = os.path.dirname(os.path.realpath(__file__))
main_dir_path = os.path.dirname(doc_dir_path)
mepod_dir_path = os.path.join(main_dir_path, "src", "mepo")
command_dir_path = os.path.join(mepod_dir_path, "command")


def get_command_list(directory):
    all_commands_py = glob.glob(os.path.join(directory, "*.py"))
    commands = {os.path.basename(x)[:-3] for x in all_commands_py}
    groups = {name.split("_", 1)[0] for name in commands if "_" in name}
    return sorted(
        name.replace("_", " ")
        for name in commands
        if not name.startswith("_") and name not in groups
    )


def create_markdown_from_usage(command, mdFile):
    cmd = [sys.executable, "-m", "mepo", *command.split(), "--help"]
    result = sp.run(
        cmd, capture_output=True, universal_newlines=True, check=True, cwd=main_dir_path
    )
    output = result.stdout.replace("__main__.py", "mepo")
    usage, summary, *_ = output.strip().split("\n\n")
    mdFile.write(summary)

    # Usage
    usage = usage.replace("usage: ", "")
    mdFile.new_header(level=3, title="Usage")
    mdFile.insert_code(usage)

    positional_arguments = output.partition("positional arguments:\n")[2].partition(
        "\n\n"
    )[0]
    if positional_arguments:
        mdFile.new_header(level=3, title="Positional Arguments")
        mdFile.insert_code(positional_arguments)

    optional_arguments = output.partition("options:\n")[2].partition("\n\n")[0]
    if not optional_arguments:
        optional_arguments = output.partition("optional arguments:\n")[2].partition(
            "\n\n"
        )[0]
    # Remove extra blank lines
    optional_arguments = os.linesep.join(
        [s for s in optional_arguments.splitlines() if s]
    )
    if optional_arguments:
        mdFile.new_header(level=3, title="Optional Arguments")
        mdFile.insert_code(optional_arguments)


if __name__ == "__main__":

    doc_file = "Mepo-Commands.md"
    mdFile = MdUtils(file_name=doc_file)

    mdFile.new_header(level=1, title="Overview")
    mdFile.new_paragraph(preamble)

    mdFile.new_header(level=1, title="Commands")
    command_list = get_command_list(command_dir_path)
    for command in command_list:
        mdFile.new_header(level=2, title=command)
        print(f"mepo command: {command}")
        create_markdown_from_usage(command, mdFile)

    mdFile.new_table_of_contents(table_title="Table of Contents", depth=2)
    mdFile.create_md_file()
    print(f"Generated {doc_file}.")

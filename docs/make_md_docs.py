#!/usr/bin/env python3

import os
import io
import glob
from mdutils.mdutils import MdUtils
import subprocess as sp

preamble='''
mepo provides many different commands for working with a multi-repository fixture.
'''

# Assume this script is in mepo/doc. Then we need to get to the mepo/mepo.d/command directory
doc_dir_path = os.path.dirname(os.path.realpath(__file__))
# Then we need to get to the mepo/mepo.d/command directory. First the "main" dir
main_dir_path = os.path.dirname(doc_dir_path)
# Now add "src/mepo"
mepod_dir_path = os.path.join(main_dir_path, "src", "mepo")
# And then "command"
command_dir_path = os.path.join(mepod_dir_path, "command")

mepo_command_path = os.path.join(main_dir_path, "bin", "mepo")

def get_command_list(directory):
    # # Walk the tree
    # roots = [x[0] for x in os.walk(directory)]

    # # Now remove "." from the list
    # roots = roots[1:]
    # print(f"roots: {roots}")

    # # Just get the relative paths
    # rel_roots = [os.path.relpath(x,directory) for x in roots]
    # print(f"rel roots: {rel_roots}")

    # # Now exclude __pycache__
    # command_dirs = [x for x in rel_roots if "__pycache__" not in x]
    # print(f"command dirs: {command_dirs}")

    # Convert slashes to spaces
    all_commands_py = glob.glob(os.path.join(directory, "*.py"))
    all_commands = [os.path.basename(x).replace(".py", "") for x in all_commands_py]
    all_commands.remove("command") # manually remove
    
    # Now let"s find the commands that have subcommands
    ## First we get commands with underscore
    commands_with_underscore = [x for x in all_commands if "_" in x]
    commands_with_subcommands = [x.replace("_", " ") for x in commands_with_underscore]

    # Now remove those from our list
    all_useful_commands = [x for x in all_commands if x not in commands_with_underscore]
    all_useful_commands += commands_with_subcommands

    return sorted(all_useful_commands)

def create_markdown_from_usage(command, mdFile):
    cmd = [mepo_command_path, command, "--help"]

    # Some commands have spaces, so we need to break it up again
    cmd = " ".join(cmd).split()
    print(f"command: {cmd}")

    result = sp.run(cmd, capture_output=True, universal_newlines=True, env={"COLUMNS":"256"})
    output = result.stdout
    print(f"output: {output}")

    output_list = output.split("\n")
    print(f"output list: {output_list}")

    # Command summary
    summary = output_list[2]
    mdFile.write(summary)

    # Usage
    usage = output_list[0]
    usage = usage.replace("usage: ","")
    mdFile.new_header(level=3, title="Usage")
    mdFile.insert_code(usage)

    positional_arguments = output.partition("positional arguments:\n")[2].partition("\n\n")[0]
    if positional_arguments:
        mdFile.new_header(level=3, title="Positional Arguments")
        mdFile.insert_code(positional_arguments)

    optional_arguments = output.partition("optional arguments:\n")[2].partition("\n\n")[0]
    # Remove extra blank lines
    optional_arguments = os.linesep.join([s for s in optional_arguments.splitlines() if s])
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
    print(f"command_list: {command_list}")
    for command in command_list:
        mdFile.new_header(level=2, title=command)
        create_markdown_from_usage(command,mdFile)

    mdFile.new_table_of_contents(table_title="Table of Contents", depth=2)
    mdFile.create_md_file()
    print(f"Generated {doc_file}.")

import configparser
import os

mepoconfig_file = os.path.expanduser('~/.mepoconfig')

def print_sections():
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    print(mepoconfig.sections())

def print_options(section):
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    print(mepoconfig.options(section))

def has_section(section):
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    return mepoconfig.has_section(section)

def has_option(section, option):
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    return mepoconfig.has_option(section, option)

def get(section, option):
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    return mepoconfig.get(section, option)

def get_command_alias(command):
    output = []
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    if has_section('alias'):
        for key,value in mepoconfig.items('alias'):
            if value == command:
                output.append(key)
    return output

def get_alias_command(alias):
    mepoconfig = configparser.ConfigParser()
    mepoconfig.read(mepoconfig_file)
    command = alias
    if has_section('alias'):
        for key,value in mepoconfig.items('alias'):
            if key == alias:
                command = value
    return command

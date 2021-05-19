import os

def parse(meporc_file):
    """
    Return a dictionary after parsing the meporc file
    """
    if os.path.isfile(meporc_file):
        meporc_dict = {}
        with open(meporc_file,'r') as fh:
            for line in fh:
                key, value = line.split(':')
                meporc_dict[key.strip()] = value.strip()
        return meporc_dict
    else:
        raise FileNotFoundError('meporc file [%s] does not exist' % meporc_file)

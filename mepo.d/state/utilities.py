import os
from collections import OrderedDict

KEYLIST = ['level', 'name', 'origin', 'tag', 'branch', 'path']

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def flatten_nested_odict(nested, flat=None, keywd='Components', level=0):
    if flat is None:
        flat = OrderedDict()
    for name, repo in nested[keywd].items():
        flat[name] = OrderedDict([('level', level)])
        for key, value in repo.items():
            if key == keywd:
                flatten_nested_odict(repo, flat, keywd, level+1) # recurse
            else:
                flat[name][key] = value
    return flat

def relpath_to_abs(flat):
    for name, repo in flat.items():
        flat[name]['local'] = os.path.abspath(flat[name]['local'])
    return flat

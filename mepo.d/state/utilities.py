import os

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def flatten_nested_odict(nested, flat=None, keywd='Components', parent=None):
    if flat is None:
        flat = dict()
    for name, repo in nested[keywd].items():
        flat[name] = {'parent': parent}
        for key, value in repo.items():
            if key == keywd:
                flatten_nested_odict(repo, flat, keywd, parent=name) # recurse
            else:
                flat[name][key] = value
    return flat

def relpath_to_abs(flat):
    for name, repo in flat.items():
        flat[name]['local'] = os.path.abspath(flat[name]['local'])
    return flat

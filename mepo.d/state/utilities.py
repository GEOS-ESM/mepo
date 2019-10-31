import os

KEYLIST = ['level', 'name', 'origin', 'tag', 'branch', 'path']

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def flatten_nested_dict(nestedd, flatd=None, keywd='Components', level=0):
    if flatd is None:
        flatd = dict()
    for name, repo in nestedd[keywd].items():
        flatd[name] = dict(level = 0)
        for key, value in repo.items():
            if key == keywd:
                flatten_nested_dict(repo, flatd, keywd, level+1) # recurse
            else:
                flatd[name][key] = value
    return flatd

def relpath_to_abs(nestedd, keywd='Components'):
    for name, repo in nestedd[keywd].items():
        for key, value in repo.items():
            if key == keywd:
                relpath_to_abs(repo)
            else:
                if key == 'local':
                    repo[key] = os.path.abspath(value)
    return nestedd

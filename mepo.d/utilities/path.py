import os

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def relpath_to_abs(repolist):
    for name, repo in repolist.items():
        repolist[name]['local'] = os.path.abspath(repolist[name]['local'])
    return repolist

def abspath_to_rel(repolist, start):
    for name, repo in repolist.items():
        repolist[name]['local'] = './' + os.path.relpath(repolist[name]['local'], start)
    return repolist

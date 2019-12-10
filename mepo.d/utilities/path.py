import os

def get_parent_dirs():
    mypath = os.getcwd()
    parentdirs = [mypath]
    while mypath != '/':
        mypath = os.path.dirname(mypath)
        parentdirs.append(mypath)
    return parentdirs

def relpath_to_abs(complist):
    for name, comp in complist.items():
        comp['local'] = os.path.abspath(comp['local'])
    return complist

def abspath_to_rel(complist, start):
    for name, comp in complist.items():
        complist[name]['local'] = './' + os.path.relpath(complist[name]['local'], start)
    return complist

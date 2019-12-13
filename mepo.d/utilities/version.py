import os
import subprocess as sp
from collections import namedtuple

from repository.git import GitRepository

Version = namedtuple('Version', ['name', 'type', 'detached'])

def get_current_s(component):
    vname, vtype, detached = get_current(component)
    result = '({}) {}'.format(vtype, vname)
    if detached:
        result += ' (DH)'
    return result

def get_current(component):
    git = GitRepository(component['remote'], component['local'])
    name, tYpe, detached = git.get_version()
    return Version(name, tYpe, detached)
    
def get_original_s(component):
    original = get_original(component)
    return '({}) {}'.format(original.type, original.name)
    
def get_original(component):
    vname = component.get('branch')
    vtype = 'b'
    if vname is None:
        vname = component.get('tag')
        vtype = 't'
    # Original clones are always in detached head state
    return Version(vname, vtype, True)

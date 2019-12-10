import os
import subprocess as sp
from collections import namedtuple

Version = namedtuple('Version', ['name', 'type', 'detached_head'])

def get_current_s(component):
    vname, vtype, detached_head = get_current(component)
    if detached_head:
        return '({}) {} ({})'.format(vtype, vname, detached_head)
    else:
        return '({}) {}'.format(vtype, vname)
    
def get_current(component):
    cmd = 'git -C %s show -s --pretty=%%D HEAD' % component['local']
    output = sp.check_output(cmd.split()).decode().rstrip()
    if output.startswith('HEAD ->'): # an actual branch
        vtype = 'b'
        vname = output.split(',')[0].split('->')[1].strip()
        detached_head = None
    elif output.startswith('HEAD,'): # detached head
        vtype, vname = _parse_detached_head_info(output)
        detached_head = 'DH'
    else:
        vtype = vname = detached_head = '?'
    return Version(vname, vtype, detached_head)

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
    return Version(vname, vtype, 'DH')

def _parse_detached_head_info(output):
    tmp = output.split(',')[1].strip()
    if tmp.startswith('tag:'): # tag
        vtype = 't'
        vname = tmp[5:]
    else:
        vtype = 'b'
        vname = tmp
    return (vtype, vname)

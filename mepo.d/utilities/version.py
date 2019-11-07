import os
import subprocess as sp

def get_current_s(repo):
    vname, vtype, detached_head = get_current(repo)
    if detached_head:
        return '({}) {} ({})'.format(vtype, vname, detached_head)
    else:
        return '({}) {}'.format(vtype, vname)
    
def get_current(repo):
    cmd = 'git -C %s show -s --pretty=%%D HEAD' % repo['local']
    output = sp.check_output(cmd.split()).rstrip()
    if output.startswith('HEAD ->'): # an actual branch
        vtype = 'b'
        vname = output.split(',')[0].split('->')[1].strip()
        detached_head = None
    elif output.startswith('HEAD,'): # detached head
        vtype, vname = _parse_detached_head_info(output)
        detached_head = 'DH'
    else:
        vtype = vname = detached_head = '?'
    return (vname, vtype, detached_head)

def get_original_s(repo):
    vname, vtype = get_original(repo)
    return '({}) {}'.format(vtype, vname)
    
def get_original(repo):
    vname = repo.get('branch')
    vtype = 'b'
    if vname is None:
        vname = repo.get('tag')
        vtype = 't'
    return (vname, vtype)

def _parse_detached_head_info(output):
    tmp = output.split(',')[1].strip()
    if tmp.startswith('tag:'): # tag
        vtype = 't'
        vname = tmp[5:]
    else:
        vtype = 'b'
        vname = tmp
    return (vtype, vname)

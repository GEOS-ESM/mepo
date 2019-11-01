import os
import subprocess as sp

def get_current_version(name, repo):
    cmd = 'git -C %s show -s --pretty=%%D HEAD' % repo['local']
    output = sp.check_output(cmd.split()).rstrip()
    if output.startswith('HEAD ->'): # an actual branch
        vtype = 'b'
        vname = output.split(',')[0].split('->')[1].strip()
    elif output.startswith('HEAD,'): # detached head
        vtype, vname = __parse_detached_head_info(output)
    else:
        vtype = vname = '?'
    return '(%s) %s' % (vtype, vname)

def __parse_detached_head_info(output):
    tmp = output.split(',')[1].strip()
    if tmp.startswith('tag:'): # tag
        vtype = 't'
        vname = tmp[5:]
    else:
        vtype = 'b'
        vname = tmp
    vname += ' (DH)'
    return (vtype, vname)
    

from collections import namedtuple

MepoVersion = namedtuple('MepoVersion', ['name', 'type', 'detached'])

def version_to_string(version):
    version_name     = version[0]
    version_type     = version[1]
    version_detached = version[2]

    if version_detached: # detached head
        # We remove the "origin/" from the internal detached branch name
        # for clarity in mepo status output
        version_name = version_name.replace('origin/','')
        s = f'({version_type}) {version_name} (DH)'
    else:
        s = f'({version_type}) {version_name}'
    return s

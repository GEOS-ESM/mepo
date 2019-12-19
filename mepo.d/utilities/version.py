from collections import namedtuple

MepoVersion = namedtuple('MepoVersion', ['name', 'type', 'detached'])

def version_to_string(version):
    s = '({}) {}'.format(version[1], version[0])
    if version[2]: # detached head
        s += ' (DH)'
    return s

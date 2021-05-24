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

def sanitize_version_string(orig,curr,git):
    '''
    This routine tries to figure out if two tags are the same.

    The issue is that git sometimes returns the "wrong" tag in
    the mepo sense. mepo might have checked out tag v1.0.0 but
    if that commit is also tagged with foo, then sometimes mepo
    will say that things have changed because it thinks it's on
    foo.
    '''

    # The trick below only works on tags (I think), so
    # if not a tag, just do nothing for now
    is_tag = '(t)'

    # We pass in space-delimited strings that are:
    #  'type version dh'
    # So let's split into lists...
    orig_list = orig.split()
    curr_list = curr.split()

    # Then pull the types...
    orig_type = orig_list[0]
    curr_type = curr_list[0]

    # Now if a type...
    if orig_type == is_tag and curr_type == is_tag:

        # Pull out the version string...
        orig_ver = orig_list[1]
        curr_ver = curr_list[1]

        # Use rev-list to get the hash of the tag...
        orig_rev = git.rev_list(orig_ver)
        curr_rev = git.rev_list(curr_ver)

        # If they are identical...
        if orig_rev == curr_rev:

            # Replace the curr version with the original to make
            # mepo happy...
            curr_list[curr_list.index(curr_ver)] = orig_ver

            # And then remake the curr string
            curr = ' '.join(curr_list)

    # And return curr
    return curr

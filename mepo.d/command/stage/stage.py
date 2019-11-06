import re
import subprocess as sp

from state.state import MepoState

def run(args):
    allrepos = MepoState.read_state()
    for name, repo in allrepos.iteritems():
        file_list = __check_status(name, repo).lstrip()
        file_list = __remove_ansi_escape_seq(file_list)
        if file_list:
            print name
            __stage_files(file_list, repo)

def __check_status(name, repo):
    cmd = 'git -C %s status -s' % repo['local']
    output = sp.check_output(cmd.split())
    return output.rstrip()

def __stage_files(file_list, repo):
    for line in file_list.split('\n'):
        myfile = line.strip().split()[1]
        cmd = 'git -C %s add %s' % (repo['local'], myfile)
        sp.check_output(cmd.split())
        print '    staged %s' % myfile

def __remove_ansi_escape_seq(instr):
    # 7-bit C1 ANSI sequences
    ansi_escape = re.compile(r'''
       \x1B    # ESC
       [@-_]   # 7-bit C1 Fe
       [0-?]*  # Parameter bytes
       [ -/]*  # Intermediate bytes
       [@-~]   # Final byte
    ''', re.VERBOSE)
    return ansi_escape.sub('', instr)

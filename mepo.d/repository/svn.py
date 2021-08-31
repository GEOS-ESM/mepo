import os
import shutil
import subprocess
import shlex

from state.state import MepoState
from utilities import shellcmd
from utilities import colors
from urllib.parse import urljoin

class SVNRepository(object):
    """
    Class to consolidate svn commands
    """
    __slots__ = ['__local', '__full_local_path', '__remote', '__svn']

    def __init__(self, remote_url, local_path):
        self.__local = local_path

        self.__remote = remote_url

        root_dir = MepoState.get_root_dir()
        full_local_path=os.path.join(root_dir,local_path)
        self.__full_local_path=full_local_path
        self.__svn = 'svn -C "{}"'.format(self.__full_local_path)

    def get_local_path(self):
        return self.__local

    def get_full_local_path(self):
        return self.__full_local_path

    def get_remote_url(self):
        return self.__remote

    def clone(self, version, recurse, type):
        os.mkdir(self.__full_local_path)
        os.chdir(self.__full_local_path)
        cmd = 'svn checkout '
        if type == 'b':
            svntype = 'branches'
        elif type == 't':
            svntype == 'tags'
        else:
            raise Exception("This should not happen")
        cmd += '{}/{}/{} {}'.format(self.__remote, svntype, version, self.__full_local_path)
        shellcmd.run(shlex.split(cmd))

    def checkout(self, version, recurse, type):
        os.mkdir(self.__full_local_path)
        os.chdir(self.__full_local_path)
        cmd = 'svn checkout '
        if type == 'b':
            svntype = 'branches'
        elif type == 't':
            svntype == 'tags'
        else:
            raise Exception("This should not happen")
        cmd += '{}/{}/{} {}'.format(self.__remote, svntype, version, self.__full_local_path)
        shellcmd.run(shlex.split(cmd))

    #def sparsify(self, sparse_config):
        #dst = os.path.join(self.__local, '.git', 'info', 'sparse-checkout')
        #os.makedirs(os.path.dirname(dst), exist_ok=True)
        #shutil.copy(sparse_config, dst)
        #cmd1 = self.__git + ' config core.sparseCheckout true'
        #shellcmd.run(shlex.split(cmd1))
        #cmd2 = self.__git + ' read-tree -mu HEAD'
        #shellcmd.run(shlex.split(cmd2))

    #def list_branch(self, all=False):
        #cmd = self.__git + ' branch'
        #if all:
            #cmd += ' -a'
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def list_tags(self):
        #cmd = self.__git + ' tag'
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def rev_list(self, tag):
        #cmd = self.__git + ' rev-list -n 1 {}'.format(tag)
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def list_stash(self):
        #cmd = self.__git + ' stash list'
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def pop_stash(self):
        #cmd = self.__git + ' stash pop'
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def apply_stash(self):
        #cmd = self.__git + ' stash apply'
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def push_stash(self, message):
        #cmd = self.__git + ' stash push'
        #if message:
            #cmd += ' -m {}'.format(message)
        #return shellcmd.run(shlex.split(cmd), output=True)

    #def show_stash(self, patch):
        #cmd = self.__git + ' stash show'
        #if patch:
            #cmd += ' -p --color'
        #output = shellcmd.run(shlex.split(cmd),output=True)
        #return output.rstrip()

    def run_diff(self, args=None):
        os.chdir(self.__full_local_path)
        cmd = 'svn diff'
        if args.name_only:
            cmd += ' --summarize'
        output = shellcmd.run(shlex.split(cmd),output=True)
        return output.rstrip()

    #def verify_branch(self, branch_name):
        #cmd = self.__git + ' show-branch remotes/origin/{}'.format(branch_name)
        #status = shellcmd.run(shlex.split(cmd),status=True)
        #return status

    def check_status(self):
        cmd = 'svn status'
        output = shellcmd.run(shlex.split(cmd), output=True)
        if output.strip():
            output_list = output.splitlines()

            # Grab the file names first for pretty printing
            file_name_list = [item.split()[-1] for item in output_list]
            max_file_name_length = len(max(file_name_list, key=len))

            verbose_output_list = []
            for item in output_list:

                short_status = item.split()[0]

                file_name = item.split()[-1]

                if short_status == "?":
                    verbose_status = colors.RED   + "untracked file" + colors.RESET
                elif short_status == "!":
                    verbose_status = colors.RED   + "missing file" + colors.RESET

                elif short_status == "A":
                    verbose_status = colors.RED   + "scheduled for addition" + colors.RESET
                elif short_status == "D":
                    verbose_status = colors.RED   + "scheduled for deletion" + colors.RESET
                elif short_status == "M":
                    verbose_status = colors.RED   + "modified" + colors.RESET
                elif short_status == "R":
                    verbose_status = colors.RED   + "replaced" + colors.RESET
                elif short_status == "C":
                    verbose_status = colors.RED   + "conflict" + colors.RESET
                elif short_status == "I":
                    verbose_status = colors.RED   + "ignored" + colors.RESET
                elif short_status == "M":
                    verbose_status = colors.RED   + "modified" + colors.RESET
                elif short_status == "M":
                    verbose_status = colors.RED   + "modified" + colors.RESET

                else:
                    verbose_status = colors.CYAN + "unknown" + colors.RESET + " (please contact mepo maintainer)"

                verbose_status_string = "{file_name:>{file_name_length}}: {verbose_status}".format(
                        file_name=file_name, file_name_length=max_file_name_length,
                        verbose_status=verbose_status)
                verbose_output_list.append(verbose_status_string)

            output = "\n".join(verbose_output_list)

        return output.rstrip()

    #def __get_modified_files(self):
        #cmd = self.__git + ' diff --name-only'
        #output = shellcmd.run(shlex.split(cmd), output=True).strip()
        #return output.split('\n') if output else []

    #def __get_untracked_files(self):
        #cmd = self.__git + ' ls-files --others --exclude-standard'
        #output = shellcmd.run(shlex.split(cmd), output=True).strip()
        #return output.split('\n') if output else []

    #def get_changed_files(self, untracked=False):
        #changed_files = self.__get_modified_files()
        #if untracked:
            #changed_files += self.__get_untracked_files()
        #return changed_files

    #def stage_file(self, myfile):
        #cmd = self.__git + ' add {}'.format(myfile)
        #shellcmd.run(shlex.split(cmd))

    #def get_staged_files(self):
        #cmd = self.__git + ' diff --name-only --staged'
        #output = shellcmd.run(shlex.split(cmd), output=True).strip()
        #return output.split('\n') if output else []

    #def unstage_file(self, myfile):
        #cmd = self.__git + ' reset -- {}'.format(myfile)
        #shellcmd.run(shlex.split(cmd))

    #def commit_files(self, message, tf_file=None):
        #if tf_file:
            #cmd = ['git', '-C', self.__full_local_path, 'commit', '-F', tf_file]
        #elif message:
            #cmd = ['git', '-C', self.__full_local_path, 'commit', '-m', message]
        #else:
            #raise Exception("This should not happen")
        #shellcmd.run(cmd)

    #def push(self):
        #cmd = self.__git + ' push -u {}'.format(self.__remote)
        #return shellcmd.run(shlex.split(cmd), output=True).strip()

    #def get_remote_latest_commit_id(self, branch, commit_type):
        #if commit_type == 'h':
            #cmd = self.__git + ' cat-file -e {}'.format(branch)
            #status = shellcmd.run(shlex.split(cmd), status=True)
            #if status != 0:
                #msg = 'Hash {} does not exist on {}'.format(branch, self.__remote)
                #msg += " Have you run 'mepo push'?"
                #raise RuntimeError(msg)
            #return branch
        #else:
            ## If we are a branch...
            #if commit_type == 'b':
                #msgtype = "Branch"
                #reftype = 'heads'
            #elif commit_type == 't':
                #msgtype = 'Tag'
                #reftype = 'tags'
            #else:
                #raise RuntimeError("Should not get here")
            #cmd = self.__git + ' ls-remote {} refs/{}/{}'.format(self.__remote, reftype, branch)
            #output = shellcmd.run(shlex.split(cmd), output=True).strip()
            #if not output:
                #msg = '{} {} does not exist on {}'.format(msgtype, branch, self.__remote)
                #msg += " Have you run 'mepo push'?"
                #raise RuntimeError(msg)
            #return output.split()[0]

    #def get_local_latest_commit_id(self):
        #cmd = self.__git + ' rev-parse HEAD'
        #return shellcmd.run(shlex.split(cmd), output=True).strip()

    #def pull(self):
        #cmd = self.__git + ' pull'
        #return shellcmd.run(shlex.split(cmd), output=True).strip()

    def get_version(self):
        detached = False
        os.chdir(self.__full_local_path)
        cmd = "svn info"
        output = shellcmd.run(shlex.split(cmd), output=True)
        for line in output.splitlines():
            if line.startswith('URL: '):
                svnurl = line.split()[-1]
        detached = False
        if 'branches' in svnurl:
            tYpe = 'b'
        elif 'tags' in svnurl:
            tYpe = 't'
        else:
            raise Exception("This should not happen")
        name = svnurl.split('/')[-1].strip()
        return (name, tYpe, detached)

#def get_current_remote_url():
    #cmd = 'git remote get-url origin'
    #output = shellcmd.run(shlex.split(cmd), output=True).strip()
    #return output

import os
import shutil

from utilities import shellcmd

class GitRepository(object):
    """
    Class to consolidate git commands
    """
    __slots__ = ['__local', '__remote', '__git']

    def __init__(self, remote_url, local_path):
        self.__local = local_path
        self.__remote = remote_url
        self.__git = 'git -C {}'.format(local_path)

    def get_local_path(self):
        return self.__local

    def get_remote_url(self):
        return self.__remote

    def clone(self):
        cmd = 'git clone --quiet {} {}'.format(self.__remote, self.__local)
        shellcmd.run(cmd.split())

    def checkout(self, version):
        cmd = self.__git + ' checkout --quiet {}'.format(version)
        shellcmd.run(cmd.split())

    def sparsify(self, sparse_config):
        dst = os.path.join(self.__local, '.git', 'info', 'sparse-checkout')
        shutil.copy(sparse_config, dst)
        cmd1 = self.__git + ' config core.sparseCheckout true'
        shellcmd.run(cmd1.split())
        cmd2 = self.__git + ' read-tree -mu HEAD'
        shellcmd.run(cmd2.split())

    def list_branch(self, all=False):
        cmd = self.__git + ' branch'
        if all:
            cmd += ' -a'
        return shellcmd.run(cmd.split(), output=True)

    def create_branch(self, branch_name):
        cmd = self.__git + ' branch {}'.format(branch_name)
        shellcmd.run(cmd.split())

    def delete_branch(self, branch_name, force):
        delete = '-d'
        if force:
            delete = '-D'
        cmd = self.__git + ' branch {} {}'.format(delete, branch_name)
        shellcmd.run(cmd.split())

    def check_status(self):
        cmd = self.__git + ' status -s'
        output = shellcmd.run(cmd.split(), output=True)
        return output.rstrip()

    def __get_modified_files(self):
        cmd = self.__git + ' diff --name-only'
        output = shellcmd.run(cmd.split(), output=True).strip()
        return output.split('\n') if output else []

    def __get_untracked_files(self):
        cmd = self.__git + ' ls-files --others --exclude-standard'
        output = shellcmd.run(cmd.split(), output=True).strip()
        return output.split('\n') if output else []

    def get_changed_files(self, untracked=False):
        changed_files = self.__get_modified_files()
        if untracked:
            changed_files += self.__get_untracked_files()
        return changed_files

    def stage_file(self, myfile):
        cmd = self.__git + ' add {}'.format(myfile)
        shellcmd.run(cmd.split())

    def get_staged_files(self):
        cmd = self.__git + ' diff --name-only --staged'
        output = shellcmd.run(cmd.split(), output=True).strip()
        return output.split('\n') if output else []

    def unstage_file(self, myfile):
        cmd = self.__git + ' reset -- {}'.format(myfile)
        shellcmd.run(cmd.split())

    def commit_files(self, message):
        cmd = ['git', '-C', self.__local, 'commit', '-m', message]
        shellcmd.run(cmd)

    def push(self):
        cmd = self.__git + ' push -u {}'.format(self.__remote)
        return shellcmd.run(cmd.split(), output=True).strip()

    def get_remote_latest_commit_id(self, branch):
        cmd = self.__git + ' ls-remote {} refs/heads/{}'.format(self.__remote, branch)
        output = shellcmd.run(cmd.split(), output=True).strip()
        if not output:
            msg = 'Branch {} does not exist on {}'.format(branch, self.__remote)
            msg += " Have you run 'mepo push'?"
            raise RuntimeError(msg)
        return output.split()[0]

    def get_local_latest_commit_id(self):
        cmd = self.__git + ' rev-parse HEAD'
        return shellcmd.run(cmd.split(), output=True).strip()

    def pull(self):
        cmd = self.__git + ' pull'
        shellcmd.run(cmd.split())

    def get_version(self):
        cmd = self.__git + ' show -s --pretty=%D HEAD'
        output = shellcmd.run(cmd.split(), output=True)
        if output.startswith('HEAD ->'): # an actual branch
            detached = False
            name = output.split(',')[0].split('->')[1].strip()
            tYpe = 'b'
        elif output.startswith('HEAD,'): # detached head
            detached = True
            tmp = output.split(',')[1].strip()
            if tmp.startswith('tag:'): # tag
                name = tmp[5:]
                tYpe = 't'
            else:
                name = tmp
                tYpe = 'b'
        return (name, tYpe, detached)

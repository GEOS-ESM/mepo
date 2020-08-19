import os
import shutil
import subprocess

from utilities import shellcmd
from utilities import colors
from urllib.parse import urljoin

class GitRepository(object):
    """
    Class to consolidate git commands
    """
    __slots__ = ['__local', '__remote', '__git']

    def __init__(self, remote_url, local_path):
        self.__local = local_path
        if remote_url.startswith('..'):
            rel_remote = os.path.basename(remote_url)
            fixture_url = get_current_remote_url()
            self.__remote = urljoin(fixture_url,rel_remote)
        else:
            self.__remote = remote_url
        self.__git = 'git -C {}'.format(local_path)

    def get_local_path(self):
        return self.__local

    def get_remote_url(self):
        return self.__remote

    def clone(self, recurse):
        cmd = 'git clone '
        if recurse:
            cmd += '--recurse-submodules '
        cmd += '--quiet {} {}'.format(self.__remote, self.__local)
        shellcmd.run(cmd.split())

    def checkout(self, version):
        cmd = self.__git + ' checkout --quiet {}'.format(version)
        shellcmd.run(cmd.split())

    def sparsify(self, sparse_config):
        dst = os.path.join(self.__local, '.git', 'info', 'sparse-checkout')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
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

    def list_tags(self):
        cmd = self.__git + ' tag'
        return shellcmd.run(cmd.split(), output=True)

    def list_stash(self):
        cmd = self.__git + ' stash list'
        return shellcmd.run(cmd.split(), output=True)

    def pop_stash(self):
        cmd = self.__git + ' stash pop'
        return shellcmd.run(cmd.split(), output=True)

    def apply_stash(self):
        cmd = self.__git + ' stash apply'
        return shellcmd.run(cmd.split(), output=True)

    def push_stash(self, message):
        cmd = self.__git + ' stash push'
        if message:
            cmd += ' -m {}'.format(message)
        return shellcmd.run(cmd.split(), output=True)

    def show_stash(self, patch):
        cmd = self.__git + ' stash show'
        if patch:
            cmd += ' -p --color'
        output = shellcmd.run(cmd.split(),output=True)
        return output.rstrip()

    def run_diff(self, args=None):
        cmd = self.__git + ' diff --color'
        if args.name_only:
            cmd += ' --name-only'
        output = shellcmd.run(cmd.split(),output=True)
        return output.rstrip()

    def fetch(self, args=None):
        cmd = self.__git + ' fetch'
        if args.all:
            cmd += ' --all'
        if args.prune:
            cmd += ' --prune'
        if args.tags:
            cmd += ' --tags'
        return shellcmd.run(cmd.split(), output=True)

    def create_branch(self, branch_name):
        cmd = self.__git + ' branch {}'.format(branch_name)
        shellcmd.run(cmd.split())

    def create_tag(self, tag_name, annotate, message, tf_file=None):
        if annotate:
            if tf_file:
                cmd = ['git', '-C', self.__local, 'tag', '-a', '-F', tf_file, tag_name]
            elif message:
                cmd = ['git', '-C', self.__local, 'tag', '-a', '-m', message, tag_name]
            else:
                raise Exception("This should not happen")
        else:
            cmd = ['git', '-C', self.__local, 'tag', tag_name]
        shellcmd.run(cmd)

    def delete_branch(self, branch_name, force):
        delete = '-d'
        if force:
            delete = '-D'
        cmd = self.__git + ' branch {} {}'.format(delete, branch_name)
        shellcmd.run(cmd.split())

    def delete_tag(self, tag_name):
        cmd = self.__git + ' tag -d {}'.format(tag_name)
        shellcmd.run(cmd.split())

    def verify_branch(self, branch_name):
        cmd = self.__git + ' show-branch remotes/origin/{}'.format(branch_name)
        status = shellcmd.run(cmd.split(),status=True)
        return status

    def check_status(self):
        cmd = self.__git + ' status --porcelain=v2'
        output = shellcmd.run(cmd.split(), output=True)
        if output.strip():
            output_list = output.splitlines()

            # Grab the file names first for pretty printing
            file_name_list = [item.split()[-1] for item in output_list]
            max_file_name_length = len(max(file_name_list, key=len))

            verbose_output_list = []
            for item in output_list:

                index_field = item.split()[0]
                if index_field == "2":
                    new_file_name = colors.YELLOW + item.split()[-2] + colors.RESET

                file_name = item.split()[-1]

                short_status = item.split()[1]

                #print("file: ", file_name, "short_status:", short_status, "index_field:", index_field)

                if index_field == "?":
                    verbose_status = colors.RED   + "untracked file" + colors.RESET

                elif short_status == ".D":
                    verbose_status = colors.RED   + "deleted, not staged" + colors.RESET
                elif short_status == ".M":
                    verbose_status = colors.RED   + "modified, not staged" + colors.RESET
                elif short_status == ".A":
                    verbose_status = colors.RED   + "added, not staged" + colors.RESET

                elif short_status == "D.":
                    verbose_status = colors.GREEN + "deleted, staged" + colors.RESET
                elif short_status == "M.":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET
                elif short_status == "A.":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET

                elif short_status == "MM":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "MD":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                elif short_status == "AM":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "AD":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                elif short_status == "R.":
                    verbose_status = colors.GREEN + "renamed" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET
                elif short_status == "RM":
                    verbose_status = colors.GREEN + "renamed, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "RD":
                    verbose_status = colors.GREEN + "renamed, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                elif short_status == "C.":
                    verbose_status = colors.GREEN + "copied" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET
                elif short_status == "CM":
                    verbose_status = colors.GREEN + "copied, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " with " + colors.RED + "unstaged changes" + colors.RESET
                elif short_status == "CD":
                    verbose_status = colors.GREEN + "copied, staged" + colors.RESET + " as " + colors.YELLOW + new_file_name + colors.RESET + " but " + colors.RED + "deleted, not staged" + colors.RESET

                else:
                    verbose_status = colors.CYAN + "unknown" + colors.RESET + " (please contact mepo maintainer)"

                verbose_status_string = "{file_name:>{file_name_length}}: {verbose_status}".format(
                        file_name=file_name, file_name_length=max_file_name_length, 
                        verbose_status=verbose_status)
                verbose_output_list.append(verbose_status_string)

            output = "\n".join(verbose_output_list)

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

    def commit_files(self, message, tf_file=None):
        if tf_file:
            cmd = ['git', '-C', self.__local, 'commit', '-F', tf_file]
        elif message:
            cmd = ['git', '-C', self.__local, 'commit', '-m', message]
        else:
            raise Exception("This should not happen")
        shellcmd.run(cmd)

    def push(self,tags):
        if tags:
            cmd = self.__git + ' push --tags {}'.format(self.__remote)
        else:
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
        elif output.startswith('HEAD'): # Assume hash
            cmd = self.__git + ' rev-parse --short HEAD'
            hash_out = shellcmd.run(cmd.split(), output=True)
            detached = True
            name = hash_out.rstrip()
            tYpe = 'h'
        return (name, tYpe, detached)

def get_current_remote_url():
    cmd = 'git remote get-url origin'
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output

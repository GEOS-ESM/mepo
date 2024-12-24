import os
import shutil
import shlex
import subprocess as sp

from urllib.parse import urljoin

from .utilities import shellcmd
from .utilities import colors
from .utilities.exceptions import RepoAlreadyClonedError


def get_editor():
    """
    Return GIT_EDITOR
    """
    result = sp.run(
        "git var GIT_EDITOR".split(), stdout=sp.PIPE, stderr=sp.PIPE, check=True
    )
    return result.stdout.rstrip().decode("utf-8")  # byte to utf-8


def get_current_remote_url():
    cmd = "git remote get-url origin"
    output = shellcmd.run(shlex.split(cmd), output=True).strip()
    return output


class GitRepository:
    """
    Class to consolidate git commands
    """

    __slots__ = ["__local_path_abs", "__remote", "__git"]

    def __init__(self, remote_url, local_path_abs):
        self.__local_path_abs = local_path_abs
        self.__remote = remote_url
        self.__git = 'git -C "{}"'.format(self.__local_path_abs)

    def get_local_path(self):
        return self.__local_path_abs

    def get_remote_url(self):
        return self.__remote

    def clone(self, version=None, recurse=None, partial=None):
        """
        Execute `git clone` command
        version is tag or branch
        """
        PARTIAL = {"blobless": " --filter=blob:none", "treeless": " --filter=tree:0"}

        cmd = "git clone "
        if partial is not None:
            cmd += PARTIAL[partial]
        if recurse is not None:
            cmd += " --recurse-submodules "
        cmd += " --quiet {} {}".format(self.__remote, self.__local_path_abs)
        shellcmd.run(shlex.split(cmd))

        if version is not None:
            self.checkout(version)

    def checkout(self, version, detach=False):
        cmd = self.__git + " checkout "
        cmd += "--quiet {}".format(version)
        shellcmd.run(shlex.split(cmd))
        if detach:
            cmd2 = self.__git + " checkout --detach"
            shellcmd.run(shlex.split(cmd2))

    def sparsify(self, sparse_config):
        dst = os.path.join(self.__local_path_abs, ".git", "info", "sparse-checkout")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(sparse_config, dst)
        cmd1 = self.__git + " config core.sparseCheckout true"
        shellcmd.run(shlex.split(cmd1))
        cmd2 = self.__git + " read-tree -mu HEAD"
        shellcmd.run(shlex.split(cmd2))

    def list_branch(self, all=False, nocolor=False):
        cmd = self.__git + " branch"
        if all:
            cmd += " -a"
        if nocolor:
            cmd += " --color=never"
        return shellcmd.run(shlex.split(cmd), output=True)

    def list_tags(self):
        cmd = self.__git + " tag"
        return shellcmd.run(shlex.split(cmd), output=True)

    def rev_list(self, tag):
        cmd = self.__git + " rev-list -n 1 {}".format(tag)
        return shellcmd.run(shlex.split(cmd), output=True)

    def rev_parse(self, short=False):
        cmd = self.__git + " rev-parse --verify HEAD"
        if short:
            cmd += " --short"
        return shellcmd.run(shlex.split(cmd), output=True)

    def list_stash(self):
        cmd = self.__git + " stash list"
        return shellcmd.run(shlex.split(cmd), output=True)

    def pop_stash(self):
        cmd = self.__git + " stash pop"
        return shellcmd.run(shlex.split(cmd), output=True)

    def apply_stash(self):
        cmd = self.__git + " stash apply"
        return shellcmd.run(shlex.split(cmd), output=True)

    def push_stash(self, message):
        cmd = self.__git + " stash push"
        if message:
            cmd += " -m {}".format(message)
        return shellcmd.run(shlex.split(cmd), output=True)

    def show_stash(self, patch):
        cmd = self.__git + " stash show"
        if patch:
            cmd += " -p --color"
        output = shellcmd.run(shlex.split(cmd), output=True)
        return output.rstrip()

    def run_diff(self, args=None, ignore_submodules=False):
        cmd = "git -C {}".format(self.__local_path_abs)
        if args.ignore_permissions:
            cmd += " -c core.fileMode=false"
        cmd += " diff --color"
        if args.name_only:
            cmd += " --name-only"
        if args.name_status:
            cmd += " --name-status"
        if args.staged:
            cmd += " --staged"
        if args.ignore_space_change:
            cmd += " --ignore-space-change"
        if ignore_submodules:
            cmd += " --ignore-submodules=all"
        output = shellcmd.run(shlex.split(cmd), output=True)
        return output.rstrip()

    def fetch(self, args=None):
        cmd = self.__git + " fetch"
        if args.all:
            cmd += " --all"
        if args.prune:
            cmd += " --prune"
        if args.tags:
            cmd += " --tags"
        if args.force:
            cmd += " --force"
        return shellcmd.run(shlex.split(cmd), output=True)

    def create_branch(self, branch_name):
        cmd = self.__git + " branch {}".format(branch_name)
        shellcmd.run(shlex.split(cmd))

    def create_tag(self, tag_name, annotate, message, tf_file=None):
        if annotate:
            if tf_file:
                cmd = [
                    "git",
                    "-C",
                    self.__local_path_abs,
                    "tag",
                    "-a",
                    "-F",
                    tf_file,
                    tag_name,
                ]
            elif message:
                cmd = [
                    "git",
                    "-C",
                    self.__local_path_abs,
                    "tag",
                    "-a",
                    "-m",
                    message,
                    tag_name,
                ]
            else:
                raise Exception("This should not happen")
        else:
            cmd = ["git", "-C", self.__local_path_abs, "tag", tag_name]
        shellcmd.run(cmd)

    def delete_branch(self, branch_name, force):
        delete = "-d"
        if force:
            delete = "-D"
        cmd = self.__git + " branch {} {}".format(delete, branch_name)
        shellcmd.run(shlex.split(cmd))

    def delete_tag(self, tag_name):
        cmd = self.__git + " tag -d {}".format(tag_name)
        shellcmd.run(shlex.split(cmd))

    def push_tag(self, tag_name, force, delete):
        cmd = self.__git + " push"
        if force:
            cmd += " --force"
        if delete:
            cmd += " --delete"
        cmd += " origin {}".format(tag_name)
        shellcmd.run(shlex.split(cmd))

    def verify_branch_or_tag(self, ref_name):
        branch_cmd = self.__git + f" show-branch remotes/origin/{ref_name}"
        tag_cmd = self.__git + f" rev-parse {ref_name}"
        branch_status = shellcmd.run(shlex.split(branch_cmd), status=True)
        ref_type = "UNKNOWN"
        if branch_status != 0:
            status = shellcmd.run(shlex.split(tag_cmd), status=True)
            ref_type = "Tag"
        else:
            status = branch_status
            ref_type = "Branch"
        return status, ref_type

    def check_status(self, ignore_permissions=False, ignore_submodules=False):
        cmd = "git -C {}".format(self.__local_path_abs)
        if ignore_permissions:
            cmd += " -c core.fileMode=false"
        cmd += " status --porcelain=v2"
        if ignore_submodules:
            cmd += " --ignore-submodules=all"
        output = shellcmd.run(shlex.split(cmd), output=True)
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

                if index_field == "?":
                    verbose_status = colors.RED + "untracked file" + colors.RESET

                elif short_status == ".D":
                    verbose_status = colors.RED + "deleted, not staged" + colors.RESET
                elif short_status == ".M":
                    verbose_status = colors.RED + "modified, not staged" + colors.RESET
                elif short_status == ".A":
                    verbose_status = colors.RED + "added, not staged" + colors.RESET
                elif short_status == ".T":
                    verbose_status = (
                        colors.RED + "typechange, not staged" + colors.RESET
                    )

                elif short_status == "D.":
                    verbose_status = colors.GREEN + "deleted, staged" + colors.RESET
                elif short_status == "M.":
                    verbose_status = colors.GREEN + "modified, staged" + colors.RESET
                elif short_status == "A.":
                    verbose_status = colors.GREEN + "added, staged" + colors.RESET
                elif short_status == "T.":
                    verbose_status = colors.GREEN + "typechange, staged" + colors.RESET

                elif short_status == "MM":
                    verbose_status = (
                        colors.GREEN
                        + "modified, staged"
                        + colors.RESET
                        + " with "
                        + colors.RED
                        + "unstaged changes"
                        + colors.RESET
                    )
                elif short_status == "MD":
                    verbose_status = (
                        colors.GREEN
                        + "modified, staged"
                        + colors.RESET
                        + " but "
                        + colors.RED
                        + "deleted, not staged"
                        + colors.RESET
                    )

                elif short_status == "AM":
                    verbose_status = (
                        colors.GREEN
                        + "added, staged"
                        + colors.RESET
                        + " with "
                        + colors.RED
                        + "unstaged changes"
                        + colors.RESET
                    )
                elif short_status == "AD":
                    verbose_status = (
                        colors.GREEN
                        + "added, staged"
                        + colors.RESET
                        + " but "
                        + colors.RED
                        + "deleted, not staged"
                        + colors.RESET
                    )

                elif short_status == "TM":
                    verbose_status = (
                        colors.GREEN
                        + "typechange, staged"
                        + colors.RESET
                        + " with "
                        + colors.RED
                        + "unstaged changes"
                        + colors.RESET
                    )
                elif short_status == "TD":
                    verbose_status = (
                        colors.GREEN
                        + "typechange, staged"
                        + colors.RESET
                        + " but "
                        + colors.RED
                        + "deleted, not staged"
                        + colors.RESET
                    )

                elif short_status == "R.":
                    verbose_status = (
                        colors.GREEN
                        + "renamed"
                        + colors.RESET
                        + " as "
                        + colors.YELLOW
                        + new_file_name
                        + colors.RESET
                    )
                elif short_status == "RM":
                    verbose_status = (
                        colors.GREEN
                        + "renamed, staged"
                        + colors.RESET
                        + " as "
                        + colors.YELLOW
                        + new_file_name
                        + colors.RESET
                        + " with "
                        + colors.RED
                        + "unstaged changes"
                        + colors.RESET
                    )
                elif short_status == "RD":
                    verbose_status = (
                        colors.GREEN
                        + "renamed, staged"
                        + colors.RESET
                        + " as "
                        + colors.YELLOW
                        + new_file_name
                        + colors.RESET
                        + " but "
                        + colors.RED
                        + "deleted, not staged"
                        + colors.RESET
                    )

                elif short_status == "C.":
                    verbose_status = (
                        colors.GREEN
                        + "copied"
                        + colors.RESET
                        + " as "
                        + colors.YELLOW
                        + new_file_name
                        + colors.RESET
                    )
                elif short_status == "CM":
                    verbose_status = (
                        colors.GREEN
                        + "copied, staged"
                        + colors.RESET
                        + " as "
                        + colors.YELLOW
                        + new_file_name
                        + colors.RESET
                        + " with "
                        + colors.RED
                        + "unstaged changes"
                        + colors.RESET
                    )
                elif short_status == "CD":
                    verbose_status = (
                        colors.GREEN
                        + "copied, staged"
                        + colors.RESET
                        + " as "
                        + colors.YELLOW
                        + new_file_name
                        + colors.RESET
                        + " but "
                        + colors.RED
                        + "deleted, not staged"
                        + colors.RESET
                    )

                else:
                    verbose_status = (
                        colors.CYAN
                        + "unknown"
                        + colors.RESET
                        + " (please contact mepo maintainer)"
                    )

                verbose_status_string = (
                    "{file_name:>{file_name_length}}: {verbose_status}".format(
                        file_name=file_name,
                        file_name_length=max_file_name_length,
                        verbose_status=verbose_status,
                    )
                )
                verbose_output_list.append(verbose_status_string)

            output = "\n".join(verbose_output_list)

        return output.rstrip()

    def __get_modified_files(self, orig_ver, comp_type):
        if not orig_ver:
            cmd = self.__git + " diff --name-only"
        else:
            if comp_type == "b":
                cmd = self.__git + " diff --name-only origin/{}".format(orig_ver)
            else:
                cmd = self.__git + " diff --name-only {}".format(orig_ver)
        output = shellcmd.run(shlex.split(cmd), output=True).strip()
        return output.split("\n") if output else []

    def __get_untracked_files(self):
        cmd = self.__git + " ls-files --others --exclude-standard"
        output = shellcmd.run(shlex.split(cmd), output=True).strip()
        return output.split("\n") if output else []

    def get_changed_files(self, untracked=False, orig_ver=None, comp_type=None):
        changed_files = self.__get_modified_files(orig_ver, comp_type)
        if untracked:
            changed_files += self.__get_untracked_files()
        return changed_files

    def stage_file(self, myfile):
        cmd = self.__git + " add {}".format(myfile)
        shellcmd.run(shlex.split(cmd))

    def get_staged_files(self):
        cmd = self.__git + " diff --name-only --staged"
        output = shellcmd.run(shlex.split(cmd), output=True).strip()
        return output.split("\n") if output else []

    def unstage_file(self, myfile):
        cmd = self.__git + " reset -- {}".format(myfile)
        shellcmd.run(shlex.split(cmd))

    def commit_files(self, message, tf_file=None):
        if tf_file:
            cmd = ["git", "-C", self.__local_path_abs, "commit", "-F", tf_file]
        elif message:
            cmd = ["git", "-C", self.__local_path_abs, "commit", "-m", message]
        else:
            raise Exception("This should not happen")
        shellcmd.run(cmd)

    def push(self):
        cmd = self.__git + " push -u {}".format(self.__remote)
        return shellcmd.run(shlex.split(cmd), output=True).strip()

    def get_remote_latest_commit_id(self, branch, commit_type):
        if commit_type == "h":
            cmd = self.__git + " cat-file -e {}".format(branch)
            status = shellcmd.run(shlex.split(cmd), status=True)
            if status != 0:
                msg = "Hash {} does not exist on {}".format(branch, self.__remote)
                msg += " Have you run 'mepo push'?"
                raise RuntimeError(msg)
            return branch
        else:
            # If we are a branch...
            if commit_type == "b":
                msgtype = "Branch"
                reftype = "heads"
            elif commit_type == "t":
                msgtype = "Tag"
                reftype = "tags"
            else:
                raise RuntimeError("Should not get here")
            cmd = self.__git + " ls-remote {} refs/{}/{}".format(
                self.__remote, reftype, branch
            )
            output = shellcmd.run(shlex.split(cmd), stdout=True).strip()
            if not output:
                # msg = '{} {} does not exist on {}'.format(msgtype, branch, self.__remote)
                # msg += " Have you run 'mepo push'?"
                # raise RuntimeError(msg)
                cmd = self.__git + " rev-parse HEAD"
            output = shellcmd.run(shlex.split(cmd), output=True).strip()
            return output.split()[0]

    def get_local_latest_commit_id(self):
        cmd = self.__git + " rev-parse HEAD"
        return shellcmd.run(shlex.split(cmd), output=True).strip()

    def pull(self):
        cmd = self.__git + " pull"
        return shellcmd.run(shlex.split(cmd), output=True).strip()

    def get_version(self):
        cmd = self.__git + " show -s --pretty=%D HEAD"
        output = shellcmd.run(shlex.split(cmd), output=True)
        if output.startswith("HEAD ->"):  # an actual branch
            detached = False
            name = output.split(",")[0].split("->")[1].strip()
            tYpe = "b"
        elif output.startswith("HEAD,"):  # detached head
            detached = True
            tmp = output.split(",")[1].strip()
            if tmp.startswith("tag:"):  # tag
                name = tmp[5:]
                tYpe = "t"
            else:
                # This was needed for when we weren't explicitly detaching on clone
                # cmd_for_branch = self.__git + ' reflog HEAD -n 1'
                # reflog_output = shellcmd.run(shlex.split(cmd_for_branch), output=True)
                # name = reflog_output.split()[-1].strip()
                name = output.split()[-1].strip()
                tYpe = "b"
        elif output.startswith("HEAD"):  # Assume hash
            cmd = self.__git + " rev-parse HEAD"
            hash_out = shellcmd.run(shlex.split(cmd), output=True)
            detached = True
            name = hash_out.rstrip()
            tYpe = "h"
        elif output.startswith("grafted"):
            cmd = self.__git + " describe --always"
            hash_out = shellcmd.run(shlex.split(cmd), output=True)
            detached = True
            name = hash_out.rstrip()
            tYpe = "h"
        return (name, tYpe, detached)

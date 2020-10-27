import os
from collections import namedtuple
from utilities.version import MepoVersion
from utilities import shellcmd
from urllib.parse import urlparse

class MepoComponent(object):

    __slots__ = ['name', 'local', 'remote', 'version', 'develop', 'sparse', 'recurse_submodules', 'fixture']

    def __init__(self):
        self.name = None
        self.local = None
        self.remote = None
        self.version = None
        self.develop = None
        self.sparse = None
        self.recurse_submodules = None
        self.fixture = None

    def __repr__(self):
        return '{} - local: {}, remote: {}, version: {}, develop: {}, sparse: {}, recurse_submodules: {}, fixture: {}'.format(
            self.name, self.local, self.remote, self.version, self.develop, self.sparse, self.recurse_submodules, self.fixture)

    def __set_original_version(self, comp_details):
        if self.fixture:
            cmd_if_branch = 'git symbolic-ref HEAD'
            if not shellcmd.run(cmd_if_branch.split(),status=True):
                output = shellcmd.run(cmd_if_branch.split(),output=True).rstrip()
                ver_name = output.replace('refs/heads/','')
                ver_type = 'b'
            else:
                cmd_for_tag = 'git describe --tags'
                ver_name = shellcmd.run(cmd_for_tag.split(),output=True).rstrip()
                ver_type = 't'
        else:
            if comp_details.get('branch', None):
                # SPECIAL HANDLING of 'detached head' branches
                ver_name = 'origin/' + comp_details['branch']
                ver_type = 'b'
            elif comp_details.get('hash', None):
                # Hashes don't have to exist
                ver_name = comp_details['hash']
                ver_type = 'h'
            else:
                ver_name = comp_details['tag'] # 'tag' key has to exist
                ver_type = 't'
        self.version = MepoVersion(ver_name, ver_type, True)
        
    def __validate_fixture(self, comp_details):
        unallowed_keys = ['remote', 'local', 'branch', 'hash', 'tag', 'sparse', 'recurse_submodules']
        if any([comp_details.get(key) for key in unallowed_keys]):
            raise Exception("Fixtures are only allowed fixture and develop")

    def to_component(self, comp_name, comp_details):
        self.name = comp_name
        self.fixture = comp_details.get('fixture', False)
        if self.fixture:
            self.__validate_fixture(comp_details)

            self.local = '.'
            repo_url = get_current_remote_url()
            p = urlparse(repo_url)
            last_url_node = p.path.rsplit('/')[-1]
            self.remote = "../"+last_url_node
        else:
            self.local = comp_details['local']
            self.remote = comp_details['remote']
        self.develop = comp_details.get('develop', None) # develop is optional
        self.sparse = comp_details.get('sparse', None) # sparse is optional
        self.recurse_submodules = comp_details.get('recurse_submodules', None) # recurse_submodules is optional
        self.__set_original_version(comp_details)
        return self

    def to_dict(self, start):
        details = dict()
        # Fixtures are allowed exactly two entries
        if self.fixture:
            details['fixture'] = self.fixture
            if self.develop:
                details['develop'] = self.develop
        else:
            details['local'] = self.local
            details['remote'] = self.remote
            if self.version.type == 't':
                details['tag'] = self.version.name
            elif self.version.type == 'h':
                details['hash'] = self.version.name
            else: # if not tag or hash, version has to be a branch
                if self.version.detached: # SPECIAL HANDLING of 'detached head' branches
                    details['branch'] = self.version.name.replace('origin/', '')
                else:
                    details['branch'] = self.version.name
            if self.develop:
                details['develop'] = self.develop
            if self.sparse:
                details['sparse'] = self.sparse
            if self.recurse_submodules:
                details['recurse_submodules'] = self.recurse_submodules
        return {self.name: details}

def get_current_remote_url():
    cmd = 'git remote get-url origin'
    output = shellcmd.run(cmd.split(), output=True).strip()
    return output

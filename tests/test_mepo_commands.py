import os
import sys
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(THIS_DIR, "..", "src"))
import shutil
import shlex
import unittest
import importlib
import subprocess as sp
from io import StringIO

from input import args

from mepo.command.init import run as mepo_init
from mepo.command.clone import run as mepo_clone
from mepo.command.list import run as mepo_list
from mepo.command.status import run as mepo_status
from mepo.command.compare import run as mepo_compare
from mepo.command.develop import run as mepo_develop
from mepo.command.checkout import run as mepo_checkout

import importlib
mepo_restore_state = importlib.import_module("mepo.command.restore-state")
mepo_checkout_if_exists = importlib.import_module("mepo.command.checkout-if-exists")

class TestMepoCommands(unittest.TestCase):

    maxDiff=None

    @classmethod
    def __get_saved_output(cls, output_file):
        with open(os.path.join(cls.output_dir, output_file), "r") as fin:
            saved_output = fin.read()
        return saved_output

    @classmethod
    def __checkout_fixture(cls):
        remote = 'https://github.com/GEOS-ESM/{}.git'.format(cls.fixture)
        cmd = 'git clone -b {} {} {}'.format(cls.tag, remote, cls.fixture_dir)
        sp.run(shlex.split(cmd))

    @classmethod
    def __copy_config_file(cls):
        src = os.path.join(cls.input_dir, 'components.yaml')
        dst = os.path.join(cls.fixture_dir)
        shutil.copy(src, dst)

    @classmethod
    def setUpClass(cls):
        cls.input_dir = os.path.join(THIS_DIR, 'input')
        cls.output_dir = os.path.join(THIS_DIR, 'output')
        cls.fixture = 'GEOSfvdycore'
        cls.tag = 'v1.13.0'
        cls.tmpdir = os.path.join(THIS_DIR, 'tmp')
        cls.fixture_dir = os.path.join(cls.tmpdir, cls.fixture)
        if os.path.isdir(cls.fixture_dir):
            shutil.rmtree(cls.fixture_dir)
        cls.__checkout_fixture()
        os.chdir(cls.fixture_dir)
        # mepo clone
        args.style = 'prefix'
        args.regsitry = None
        args.repo_url = None
        args.branch = None
        args.directory = None
        args.partial = 'blobless'
        mepo_clone(args)

    def setUp(self):
        pass

    def __check_status(self, saved_output_file):
        os.chdir(self.__class__.fixture_dir)
        sys.stdout = output = StringIO()
        args.ignore_permissions=False
        args.nocolor=True
        args.hashes=False
        mepo_status(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output(saved_output_file)
        self.assertEqual(output.getvalue(), saved_output)

    def __restore_state(self):
        os.chdir(self.__class__.fixture_dir)
        mepo_restore_state.run(args)
        self.__check_status("output_clone_status.txt")
    
    def test_list(self):
        os.chdir(self.__class__.fixture_dir)
        sys.stdout = output = StringIO()
        mepo_list(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_list.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_develop(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["env", "cmake", "fvdycore"]
        args.quiet = False
        mepo_develop(args)
        self.__check_status("output_develop_status.txt")
        # Clean up
        self.__restore_state()

    def test_checkout_compare(self):
        os.chdir(self.__class__.fixture_dir)
        # Checkout 'develop' branch of MAPL and env
        args.branch_name = "develop"
        args.comp_name = ["MAPL"]
        args.b = False
        args.quiet = False
        args.detach = False
        mepo_checkout(args)
        # Compare (default)
        args.all = False
        args.nocolor = True
        args.wrap = True
        sys.stdout = output = StringIO()
        mepo_compare(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_compare.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Compare (All)
        args.all = True
        sys.stdout = output = StringIO()
        mepo_compare(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_compare_all.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Clean up
        self.__restore_state()

    def test_checkout_if_exists(self):
        os.chdir(self.__class__.fixture_dir)
        args.ref_name = "aafjkgj-afgjhffg-affgurgnsfg-does-not-exist" # does not exist
        args.quiet = True
        args.detach = False
        args.dry_run = False
        mepo_checkout_if_exists.run(args)
        # Since we do not expect this ref to exist, status should be that of clone
        self.__check_status("output_clone_status.txt")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        os.chdir(THIS_DIR)
        shutil.rmtree(cls.tmpdir)

if __name__ == '__main__':
    unittest.main()

import os
import sys
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(THIS_DIR, "..", "src"))
import shutil
import shlex
import unittest
import subprocess as sp
from io import StringIO

from input import args

from mepo.command.clone import run as mepo_clone
from mepo.command.list import run as mepo_list
from mepo.command.status import run as mepo_status
from mepo.command.compare import run as mepo_compare
from mepo.command.develop import run as mepo_develop

class TestMepoCommands(unittest.TestCase):

    maxDiff=None

    @classmethod
    def __checkout_fixture(cls):
        remote = "https://github.com/pchakraborty/{}.git".format(cls.fixture)
        git_clone = "git clone "
        if cls.tag:
            git_clone += f"-b {cls.tag}"
        cmd = f"{git_clone} {remote} {cls.fixture_dir}"
        print(f"clone command: {cmd}")
        sp.run(shlex.split(cmd))

    @classmethod
    def __copy_config_file(cls):
        src = os.path.join(cls.input_dir, "components.yaml")
        dst = os.path.join(cls.fixture_dir)
        shutil.copy(src, dst)

    @classmethod
    def setUpClass(cls):
        cls.input_dir = os.path.join(THIS_DIR, "input")
        cls.output_dir = os.path.join(THIS_DIR, "output")
        cls.fixture = "GEOSfvdycore"
        cls.tag = None
        cls.tmpdir = os.path.join(THIS_DIR, "tmp")
        cls.fixture_dir = os.path.join(cls.tmpdir, cls.fixture)
        if os.path.isdir(cls.fixture_dir):
            shutil.rmtree(cls.fixture_dir)
        cls.__checkout_fixture()
        #cls.__copy_config_file()
        args.style = "prefix"
        os.chdir(cls.fixture_dir)
        args.repo_url = None
        args.branch = None
        args.directory = None
        args.partial = "blobless"
        args.registry = "components.yaml"
        mepo_clone(args)
        # In order to better test compare, we need to do *something*
        args.comp_name = ["env","FMS","fvdycore"]
        args.quiet = False
        mepo_develop(args)

    def setUp(self):
        pass

    def test_list(self):
        sys.stdout = output = StringIO()
        mepo_list(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, "list_output.txt"), "r") as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def test_status(self):
        sys.stdout = output = StringIO()
        args.ignore_permissions=False
        args.nocolor=True
        args.hashes=False
        mepo_status(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, "status_output.txt"), "r") as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def test_compare_brief(self):
        sys.stdout = output = StringIO()
        args.all=False
        args.nocolor=True
        args.wrap=True
        mepo_compare(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, "compare_brief_output.txt"), "r") as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def test_compare_full(self):
        sys.stdout = output = StringIO()
        args.all=True
        args.nocolor=True
        args.wrap=True
        mepo_compare(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, "compare_full_output.txt"), "r") as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        os.chdir(THIS_DIR)
        shutil.rmtree(cls.tmpdir)

if __name__ == "__main__":
    unittest.main()

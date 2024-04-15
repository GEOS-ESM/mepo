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
from mepo.command.branch_list import run as mepo_branch_list
from mepo.command.branch_create import run as mepo_branch_create
from mepo.command.branch_delete import run as mepo_branch_delete
from mepo.command.tag_list import run as mepo_tag_list
from mepo.command.tag_create import run as mepo_tag_create
from mepo.command.tag_delete import run as mepo_tag_delete
from mepo.command.fetch import run as mepo_fetch
from mepo.command.pull import run as mepo_pull
from mepo.command.push import run as mepo_push
from mepo.command.diff import run as mepo_diff
from mepo.command.whereis import run as mepo_whereis
from mepo.command.reset import run as mepo_reset

import importlib
mepo_restore_state = importlib.import_module("mepo.command.restore-state")
mepo_checkout_if_exists = importlib.import_module("mepo.command.checkout-if-exists")
mepo_pull_all = importlib.import_module("mepo.command.pull-all")

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
    def __mepo_clone(cls):
        # mepo clone
        args.style = 'prefix'
        args.regsitry = None
        args.repo_url = None
        args.branch = None
        args.directory = None
        args.partial = 'blobless'
        mepo_clone(args)

    @classmethod
    def setUpClass(cls):
        cls.input_dir = os.path.join(THIS_DIR, 'input')
        cls.output_dir = os.path.join(THIS_DIR, 'output')
        cls.output_clone_status = cls.__get_saved_output("output_clone_status.txt")
        cls.fixture = 'GEOSfvdycore'
        cls.tag = 'v1.13.0'
        cls.tmpdir = os.path.join(THIS_DIR, 'tmp')
        cls.fixture_dir = os.path.join(cls.tmpdir, cls.fixture)
        if os.path.isdir(cls.fixture_dir):
            shutil.rmtree(cls.fixture_dir)
        cls.__checkout_fixture()
        os.chdir(cls.fixture_dir)
        cls.__mepo_clone()

    def setUp(self):
        pass

    def __mepo_status(self, saved_output):
        '''saved_output is either a string or a filename'''
        os.chdir(self.__class__.fixture_dir)
        args.ignore_permissions = False
        args.nocolor = True
        args.hashes = False
        sys.stdout = output = StringIO()
        mepo_status(args)
        sys.stdout = sys.__stdout__
        try:
            self.assertEqual(output.getvalue(), saved_output)
        except:
            saved_output = self.__class__.__get_saved_output(saved_output)
            self.assertEqual(output.getvalue(), saved_output)

    def __mepo_restore_state(self):
        os.chdir(self.__class__.fixture_dir)
        sys.stdout = output = StringIO() # suppress output
        mepo_restore_state.run(args)
        sys.stdout == sys.__stdout__
        self.__mepo_status(self.__class__.output_clone_status)

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
        sys.stdout = output = StringIO() # suppressing output to stdout
        mepo_develop(args)
        sys.stdout = sys.__stdout__
        self.__mepo_status("output_develop_status.txt")
        # Clean up
        self.__mepo_restore_state()

    def test_checkout_compare(self):
        os.chdir(self.__class__.fixture_dir)
        # Checkout 'develop' branch of MAPL and env
        args.branch_name = "develop"
        args.comp_name = ["MAPL"]
        args.b = False
        args.quiet = False
        args.detach = False
        sys.stdout = output = StringIO() # suppress output
        mepo_checkout(args)
        sys.stdout = sys.__stdout__
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
        self.__mepo_restore_state()

    def test_checkout_if_exists(self):
        os.chdir(self.__class__.fixture_dir)
        args.ref_name = "aafjkgj-afgjhffg-affgurgnsfg-does-not-exist" # does not exist
        args.quiet = True
        args.detach = False
        args.dry_run = False
        mepo_checkout_if_exists.run(args)
        # Since we do not expect this ref to exist, status should be that of clone
        self.__mepo_status(self.__class__.output_clone_status)

    def test_branch_list(self):
        os.chdir(self.__class__.fixture_dir)
        # Not expecting new branches in this component (fingers crossed)
        args.comp_name = ["ecbuild"]
        args.all = True
        args.nocolor = True
        sys.stdout = output = StringIO()
        mepo_branch_list(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_branch_list.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_branch_create_delete(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["ecbuild"]
        args.branch_name = "the-best-branch-ever"
        # Create branch
        sys.stdout = output = StringIO()
        mepo_branch_create(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_branch_create.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Delete the branch that was just created
        args.force = False
        sys.stdout = output = StringIO()
        mepo_branch_delete(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_branch_delete.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_tag_list(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["cmake"]
        sys.stdout = output = StringIO()
        mepo_tag_list(args)
        sys.stdout = sys.__stdout__
        # Tag awesome-tag actually exists in component cmake
        self.assertTrue("awesome-tag" in output.getvalue())

    def test_tag_create_delete(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["FMS", "MAPL"]
        args.tag_name = "new-awesome-tag"
        # Create tag
        args.annotate = True
        args.message = "The new awesome tag"
        sys.stdout = output = StringIO()
        mepo_tag_create(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_tag_create.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Delete the tag that was just created
        sys.stdout = output = StringIO()
        mepo_tag_delete(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_tag_delete.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_fetch(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["FVdycoreCubed_GridComp"]
        args.all = True
        args.prune = True
        args.tags = True
        sys.stdout = output = StringIO()
        mepo_fetch(args)
        sys.stdout = sys.__stdout__
        saved_output = "Fetching \x1b[1;33mFVdycoreCubed_GridComp\x1b[0;0m\n"
        self.assertEqual(output.getvalue(), saved_output)

    def test_pull(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["FVdycoreCubed_GridComp"]
        args.quiet = False
        err_msg = "FVdycoreCubed_GridComp has detached head! Cannot pull."
        with self.assertRaisesRegex(Exception, err_msg):
            mepo_pull(args)

    def test_pull_all(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["FVdycoreCubed_GridComp"]
        args.quiet = False
        sys.stdout = output = StringIO()
        mepo_pull_all.run(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_pull_all.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_push(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = ["FVdycoreCubed_GridComp"]
        args.quiet = False
        sys.stdout = output = StringIO()
        with self.assertRaises(sp.CalledProcessError):
            mepo_push(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_push.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_diff(self):
        os.chdir(self.__class__.fixture_dir)
        os.chdir("./src/Components/@FVdycoreCubed_GridComp")
        filename = "GEOS_FV3_Utilities.F90"
        # Add a line
        with open(filename, "w") as fout:
            fout.write(" ")
        args.comp_name = ["FVdycoreCubed_GridComp"]
        args.name_only = True
        args.name_status = False
        args.ignore_permissions = False
        args.staged = False
        args.ignore_space_change = False
        sys.stdout = output = StringIO()
        mepo_diff(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_diff.txt")
        # Ignore the last line of output (horizontal line
        # with length that of the width of the terminal)
        self.assertEqual(output.getvalue().split()[:-1], saved_output.split()[:-1])
        # Clean up
        sp.run(f"git checkout {filename}".split(), stderr=sp.DEVNULL)
        self.__mepo_status(self.__class__.output_clone_status)

    def test_whereis(self):
        os.chdir(self.__class__.fixture_dir)
        args.comp_name = None
        args.ignore_case = False
        sys.stdout = output = StringIO()
        mepo_whereis(args)
        sys.stdout = sys.__stdout__
        saved_output = self.__class__.__get_saved_output("output_whereis.txt")
        self.assertEqual(output.getvalue(), saved_output)

    # def test_reset(self):
    #     os.chdir(self.__class__.fixture_dir)
    #     args.force = True
    #     args.reclone = False
    #     args.dry_run = False
    #     sys.stdout = output = StringIO()
    #     mepo_reset(args)
    #     sys.stdout = sys.__stdout__
    #     saved_output = self.__class__.__get_saved_output("output_reset.txt")
    #     self.assertEqual(output.getvalue(), saved_output)
    #     # Clean up - reclone (suppress output)
    #     sys.stdout = output = StringIO()
    #     self.__class__.__mepo_clone()
    #     sys.stdout = sys.__stdout__

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        os.chdir(THIS_DIR)
        shutil.rmtree(cls.tmpdir)

if __name__ == '__main__':
    unittest.main()

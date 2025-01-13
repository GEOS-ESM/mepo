import os

import io
import shutil
import shlex
import unittest
import importlib
import contextlib
import subprocess as sp
from types import SimpleNamespace

import mepo.command.clone as mepo_clone
import mepo.command.list as mepo_list
import mepo.command.status as mepo_status
import mepo.command.compare as mepo_compare
import mepo.command.develop as mepo_develop
import mepo.command.checkout as mepo_checkout
import mepo.command.branch_list as mepo_branch_list
import mepo.command.branch_create as mepo_branch_create
import mepo.command.branch_delete as mepo_branch_delete
import mepo.command.tag_list as mepo_tag_list
import mepo.command.tag_create as mepo_tag_create
import mepo.command.tag_delete as mepo_tag_delete
import mepo.command.fetch as mepo_fetch
import mepo.command.pull as mepo_pull
import mepo.command.push as mepo_push
import mepo.command.diff as mepo_diff
import mepo.command.whereis as mepo_whereis
import mepo.command.reset as mepo_reset
from mepo.cmdline.parser import get_version as get_mepo_version

# Import commands with dash in the name
mepo_restore_state = importlib.import_module("mepo.command.restore-state")
mepo_checkout_if_exists = importlib.import_module("mepo.command.checkout-if-exists")
mepo_pull_all = importlib.import_module("mepo.command.pull-all")

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


class TestMepoCommands(unittest.TestCase):

    @classmethod
    def __get_saved_output(cls, output_file):
        with open(os.path.join(cls.output_dir, output_file), "r") as fin:
            saved_output = fin.read()
        return saved_output

    @classmethod
    def __checkout_fixture(cls):
        remote = f"https://github.com/GEOS-ESM/{cls.fixture}.git"
        git_clone = "git clone --filter=blob:none "
        if cls.tag:
            git_clone += f"-b {cls.tag}"
        cmd = f"{git_clone} {remote} {cls.fixture_dir}"
        sp.run(shlex.split(cmd))

    @classmethod
    def __copy_config_file(cls):
        src = os.path.join(cls.input_dir, "components.yaml")
        dst = os.path.join(cls.fixture_dir)
        shutil.copy(src, dst)

    @classmethod
    def __mepo_clone(cls):
        # mepo clone
        args = SimpleNamespace(
            style="prefix",
            registry=None,
            url=None,
            allrepos=False,
            branch=None,
            directory=None,
            partial="blobless",
        )
        mepo_clone.run(args)
        print(flush=True)

    @classmethod
    def setUpClass(cls):
        cls.input_dir = os.path.join(TEST_DIR, "input")
        cls.output_dir = os.path.join(TEST_DIR, "output")
        cls.output_clone_status = cls.__get_saved_output("output_clone_status.txt")
        cls.fixture = "GEOSfvdycore"
        cls.tag = "v2.13.0"
        cls.tmpdir = os.path.join(TEST_DIR, "tmp")
        cls.fixture_dir = os.path.join(cls.tmpdir, cls.fixture)
        if os.path.isdir(cls.fixture_dir):
            shutil.rmtree(cls.fixture_dir)
        cls.__checkout_fixture()
        os.chdir(cls.fixture_dir)
        cls.__mepo_clone()

    def setUp(self):
        pass

    def __mepo_status(self, saved_output):
        """saved_output is either a string or a filename"""
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            ignore_permissions=False,
            nocolor=True,
            hashes=False,
            parallel=True,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_status.run(args)
        try:  # assume saved_output is a file
            saved_output_s = self.__class__.__get_saved_output(saved_output)
        except FileNotFoundError:
            saved_output_s = saved_output
        self.assertEqual(output.getvalue(), saved_output_s)

    def __mepo_restore_state(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(parallel=True)
        with contextlib.redirect_stdout(io.StringIO()) as _:
            mepo_restore_state.run(args)
        self.__mepo_status(self.__class__.output_clone_status)

    def test_list(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(one_per_line=False)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_list.run(args)
        saved_output = self.__class__.__get_saved_output("output_list.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_develop(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["env", "cmake", "fvdycore"],
            quiet=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as _:
            mepo_develop.run(args)
        self.__mepo_status("output_develop_status.txt")
        # Clean up
        self.__mepo_restore_state()

    def test_checkout_compare(self):
        os.chdir(self.__class__.fixture_dir)
        # Checkout "develop" branch of MAPL and env
        args = SimpleNamespace(
            branch_name="develop",
            comp_name=["MAPL"],
            b=False,
            quiet=False,
            detach=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_checkout.run(args)
        # Compare (default)
        args_cmp = SimpleNamespace(
            all=False,
            nocolor=True,
            wrap=True,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_compare.run(args_cmp)
        saved_output = self.__class__.__get_saved_output("output_compare.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Compare (All)
        args_cmp.all = True
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_compare.run(args_cmp)
        saved_output = self.__class__.__get_saved_output("output_compare_all.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Clean up
        self.__mepo_restore_state()

    def test_checkout_if_exists(self):
        # Fixture component
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            ref_name="not-expected-to-exist",
            quiet=True,
            detach=False,
            dry_run=False,
        )
        mepo_checkout_if_exists.run(args)
        # Since we do not expect this ref to exist, status should be that of clone
        self.__mepo_status(self.__class__.output_clone_status)

    def test_branch_list(self):
        os.chdir(self.__class__.fixture_dir)
        # Not expecting new branches in this component (fingers crossed)
        args = SimpleNamespace(
            comp_name=["ecbuild"],
            all=True,
            nocolor=True,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_branch_list.run(args)
        saved_output = self.__class__.__get_saved_output("output_branch_list.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_branch_create_delete(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["ecbuild"],
            branch_name="the-best-branch-ever",
        )
        # Create branch
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_branch_create.run(args)
        saved_output = self.__class__.__get_saved_output("output_branch_create.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Delete the branch that was just created
        args.force = False
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_branch_delete.run(args)
        saved_output = self.__class__.__get_saved_output("output_branch_delete.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_tag_list(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(comp_name=["env"])
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_tag_list.run(args)
        self.assertTrue("cuda11.7.0-gcc11.2.0nvptx-openmpi4.0.6" in output.getvalue())

    def test_tag_create_delete(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["FMS", "MAPL"],
            tag_name="new-awesome-tag",
            annotate=False,
            message=None,
        )
        # Create tag
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_tag_create.run(args)
        saved_output = self.__class__.__get_saved_output("output_tag_create.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Delete the tag that was just created
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_tag_delete.run(args)
        saved_output = self.__class__.__get_saved_output("output_tag_delete.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_fetch(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["FVdycoreCubed_GridComp"],
            all=True,
            prune=True,
            tags=True,
            force=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_fetch.run(args)
        saved_output = "Fetching \x1b[33mFVdycoreCubed_GridComp\x1b[0m\n"
        self.assertEqual(output.getvalue(), saved_output)

    def test_pull(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["FVdycoreCubed_GridComp"],
            quiet=False,
        )
        err_msg = "FVdycoreCubed_GridComp has detached head! Cannot pull."
        with self.assertRaisesRegex(Exception, err_msg):
            mepo_pull.run(args)

    def test_pull_all(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["FVdycoreCubed_GridComp"],
            quiet=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_pull_all.run(args)
        saved_output = self.__class__.__get_saved_output("output_pull_all.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_push(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=["FVdycoreCubed_GridComp"],
            quiet=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaises(sp.CalledProcessError):
                mepo_push.run(args)
        saved_output = self.__class__.__get_saved_output("output_push.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_diff(self):
        os.chdir(self.__class__.fixture_dir)
        os.chdir("./src/Components/@FVdycoreCubed_GridComp")
        filename = "GEOS_FV3_Utilities.F90"
        # Add a line
        with open(filename, "w") as fout:
            fout.write(" ")
        args = SimpleNamespace(
            comp_name=["FVdycoreCubed_GridComp"],
            name_only=True,
            name_status=False,
            ignore_permissions=False,
            staged=False,
            ignore_space_change=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_diff.run(args)
        saved_output = self.__class__.__get_saved_output("output_diff.txt")
        # Ignore the last line of output (horizontal line
        # with length that of the width of the terminal)
        self.assertEqual(output.getvalue().split()[:-1], saved_output.split()[:-1])
        # Clean up
        sp.run(f"git checkout {filename}".split(), stderr=sp.DEVNULL)
        self.__mepo_status(self.__class__.output_clone_status)

    def test_whereis(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            comp_name=None,
            ignore_case=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_whereis.run(args)
        saved_output = self.__class__.__get_saved_output("output_whereis.txt")
        self.assertEqual(output.getvalue(), saved_output)

    def test_reset(self):
        os.chdir(self.__class__.fixture_dir)
        args = SimpleNamespace(
            force=True,
            reclone=False,
            dry_run=False,
        )
        with contextlib.redirect_stdout(io.StringIO()) as output:
            mepo_reset.run(args)
        saved_output = self.__class__.__get_saved_output("output_reset.txt")
        self.assertEqual(output.getvalue(), saved_output)
        # Clean up - reclone (suppress output)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.__class__.__mepo_clone()

    def test_mepo_version(self):
        self.assertEqual(get_mepo_version(), "2.3.0")

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        os.chdir(TEST_DIR)
        shutil.rmtree(cls.tmpdir)


if __name__ == "__main__":
    unittest.main()

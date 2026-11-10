import os
import json
import shutil
import tempfile
import unittest
import sys
import subprocess as sp

from mepo.cmdline.completion import candidates, FILES


def names(words):
    return [name for name, _ in candidates(words)]


class TestCompletion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Fake mepo clone with a state file
        cls.cwd = os.getcwd()
        cls.tmpdir = tempfile.mkdtemp()
        os.mkdir(os.path.join(cls.tmpdir, ".mepo"))
        state = [{"name": n} for n in ("Fixture", "MAPL", "ESMA_env", "ESMA_cmake")]
        with open(os.path.join(cls.tmpdir, ".mepo", "state.json"), "w") as fout:
            json.dump(state, fout)
        os.chdir(cls.tmpdir)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.cwd)
        shutil.rmtree(cls.tmpdir)

    def test_commands(self):
        cmds = names([""])
        for cmd in ("clone", "status", "branch", "tag", "stash", "config"):
            self.assertIn(cmd, cmds)
        self.assertNotIn("--location", names(["-"]))

    def test_subcommands(self):
        self.assertEqual(names(["branch", ""]), ["list", "create", "delete"])
        self.assertEqual(names(["config", ""]), ["get", "set", "delete", "print"])
        self.assertIn("pop", names(["stash", ""]))

    def test_options(self):
        opts = names(["tag", "create", "v1", "-"])
        self.assertIn("--annotate", opts)
        self.assertIn("--message", opts)
        # already-used options are not offered again
        self.assertNotIn("--annotate", names(["tag", "create", "--annotate", "-"]))

    def test_option_values(self):
        self.assertEqual(
            names(["clone", "--style", ""]), ["naked", "prefix", "postfix"]
        )
        self.assertEqual(candidates(["clone", "--registry", ""]), FILES)
        self.assertEqual(candidates(["save", ""]), FILES)
        # option value is not mistaken for a positional
        self.assertEqual(names(["commit", "-m", "msg", "M"])[:1], ["Fixture"])

    def test_components(self):
        self.assertEqual(
            names(["develop", ""]), ["Fixture", "MAPL", "ESMA_env", "ESMA_cmake"]
        )
        # first positional of checkout is the branch, not a component
        self.assertEqual(names(["checkout", ""]), [])
        self.assertEqual(
            names(["checkout", "main", "MAPL", ""]),
            ["Fixture", "ESMA_env", "ESMA_cmake"],
        )
        self.assertEqual(names(["branch", "create", "feature/x", "E"])[0], "Fixture")

    def test_no_components_outside_clone(self):
        os.chdir(tempfile.gettempdir())
        try:
            self.assertEqual(names(["develop", ""]), [])
        finally:
            os.chdir(self.tmpdir)

    def test_entry_point(self):
        out = sp.run(
            [sys.executable, "-m", "mepo", "__complete", "branch", ""],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        self.assertEqual(
            [line.split("\t")[0] for line in out.splitlines()],
            ["list", "create", "delete"],
        )


if __name__ == "__main__":
    unittest.main()

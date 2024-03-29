import os
import sys
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(THIS_DIR, '..'))
import shutil
import shlex
import unittest
import subprocess as sp
from io import StringIO

from input import args

from command.init    import init    as mepo_init
from command.clone   import clone   as mepo_clone
from command.list    import list    as mepo_list
from command.status  import status  as mepo_status
from command.compare import compare as mepo_compare
from command.develop import develop as mepo_develop

class TestMepoCommands(unittest.TestCase):

    maxDiff=None

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
        #cls.__copy_config_file()
        args.config = 'components.yaml'
        args.style = 'prefix'
        os.chdir(cls.fixture_dir)
        mepo_init.run(args)
        args.config = None
        args.repo_url = None
        args.branch = None
        args.directory = None
        args.partial = 'blobless'
        mepo_clone.run(args)
        # In order to better test compare, we need to do *something*
        args.comp_name = ['env','cmake','fvdycore']
        args.quiet = False
        mepo_develop.run(args)

    def setUp(self):
        pass

    def test_list(self):
        sys.stdout = output = StringIO()
        mepo_list.run(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, 'list_output.txt'), 'r') as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def test_status(self):
        sys.stdout = output = StringIO()
        args.ignore_permissions=False
        args.nocolor=True
        args.hashes=False
        mepo_status.run(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, 'status_output.txt'), 'r') as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def test_compare_brief(self):
        sys.stdout = output = StringIO()
        args.all=False
        args.nocolor=True
        args.wrap=True
        mepo_compare.run(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, 'compare_brief_output.txt'), 'r') as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def test_compare_full(self):
        sys.stdout = output = StringIO()
        args.all=True
        args.nocolor=True
        args.wrap=True
        mepo_compare.run(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, 'compare_full_output.txt'), 'r') as fin:
            saved_output = fin.read()
        self.assertEqual(output.getvalue(), saved_output)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        os.chdir(THIS_DIR)
        shutil.rmtree(cls.tmpdir)

if __name__ == '__main__':
    unittest.main()

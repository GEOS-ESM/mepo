import os
import sys
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(THIS_DIR, '..'))
import shutil
import unittest
import subprocess as sp
from io import StringIO

from input import args

from command.init import init as mepo_init
from command.clone import clone as mepo_clone
from command.list import list as mepo_list
from command.status import status as mepo_status

class TestMepoCommands(unittest.TestCase):

    @classmethod
    def __checkout_fixture(cls):
        remote = 'git@github.com:GEOS-ESM/{}.git'.format(cls.fixture)
        cmd = 'git clone {} {}'.format(remote, cls.fixture_dir)
        sp.run(cmd.split())

    @classmethod
    def __copy_config_file(cls):
        src = os.path.join(cls.input_dir, 'repolist.yaml')
        dst = os.path.join(cls.fixture_dir)
        shutil.copy(src, dst)

    @classmethod
    def setUpClass(cls):
        cls.input_dir = os.path.join(THIS_DIR, 'input')
        cls.output_dir = os.path.join(THIS_DIR, 'output')
        cls.fixture = 'GEOSfvdycore'
        cls.tmpdir = os.path.join(THIS_DIR, 'tmp')
        cls.fixture_dir = os.path.join(cls.tmpdir, cls.fixture)
        if os.path.isdir(cls.fixture_dir):
            shutil.rmtree(cls.fixture_dir)
        cls.__checkout_fixture()
        cls.__copy_config_file()
        args.config_file = 'repolist.yaml'
        os.chdir(cls.fixture_dir)
        mepo_init.run(args)
        args.config = None
        mepo_clone.run(args)

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
        mepo_status.run(args)
        sys.stdout = sys.__stdout__
        with open(os.path.join(self.__class__.output_dir, 'status_output.txt'), 'r') as fin:
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

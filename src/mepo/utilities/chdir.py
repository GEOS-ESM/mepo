"""contextlib.chdir was introduced in Python 3.11"""

import os
from contextlib import contextmanager


@contextmanager
def chdir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)

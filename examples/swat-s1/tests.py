"""
swat-s1 tests.
"""

import subprocess
import sys


def test_init():

    try:
        rc = subprocess.call(sys.executable + ' run.py')
        print rc
    except Exception as error:
        print 'TEST: error: ', error

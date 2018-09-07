# pytest suite

"""
Tests for the my_module module.

This is a suite of tests to be run with pytest.

To run:
    1) set environement variable MY_TESTDATA appropriately
       Eg. export MY_TESTDATA=...path../my_testdata
    2) From the module parent directory: pytest -v --pyargs utils
"""

import os
import pytest

TESTDATAPATH = os.getenv('MY_TESTDATA', '.')

@pytest.fixture(scope='module')
def setup_module(request):
    print('setup test_init module')
    def fin():
        print('\nteardown test_init module')
    request.addfinalizer(fin)
    return

@pytest.fixture(scope='class')
def setup_testgroupoffunctions(request):
    print('setup TestGroupOfFunctions')
    def fin():
        print('\nteardown TestGroupOfFunctions')
    request.addfinalizer(fin)
    return

@pytest.fixture()
def setup_fortest(request):
    print('setup for test')
    def fin():
        print('\nteardown after test')
    request.addfinalizer(fin)
    return

@pytest.mark.usefixtures('setup_testgroupoffunctions')
class TestGroupOfFunctions():
    """
    Suite of tests for the functions in the utils.__init__ module.
    """

    def test_func1(self, setup_fortest):
        """
        Tests function func1.  (if require add details about the specific.
        of the test.
        """
        print('test_func1')

    def test_func2(self):
        """
        Tests function func2.
        """
        print('func2')

    # .... for all the function.
    # .... there can be more than one test per function just add _2 to the
    #      test name.

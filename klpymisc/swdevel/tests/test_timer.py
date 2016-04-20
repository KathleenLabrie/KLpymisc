# pytest suite for timer module

"""
Tests for the timer module.

This is a suite of tests to run with pytest.

To run:
    1) py.test -v
"""
__author__ = 'Kathleen Labrie'

import os
from klpymisc.swdevel import timer

# pylint: disable=invalid-name, no-self-use

class TestTimer(object):
    """
    Suite of tests for the Timer class
    """

    @classmethod
    def setup_class(cls):
        """
        Run once at the beginning.
        """
        pass

    @classmethod
    def teardown_class(cls):
        """
        Run once at the end.
        """
        pass

    def setup_method(self, method):
        """
        Run once before every test.
        """

    def teardown_method(self, method):
        """
        Run once after every test.
        """

    def test_init(self):
        """
        Test the basic initilization of Timer.
        """
        t = timer.Timer()
        assert t.verbose == False

    def test_enterexit(self):
        """
        Test the __enter__ and __exit__ method of Timer.
        """
        exception_type = None
        exception_value = None
        traceback = None

        t = timer.Timer()
        t.__enter__()
        t.__exit__(exception_type, exception_value, traceback)
        assert type(t.secs) == float

    def test_writelog(self):
        """
        Test the basic functionality of Timer.writelog.
        """
        expected_logstr = ['Elapse', 'time', 'for', 'TEST:', 'secs']
        expected_maxtime = 1.

        exception_type = None
        exception_value = None
        traceback = None

        t = timer.Timer()
        t.__enter__()
        t.__exit__(exception_type, exception_value, traceback)
        t.writelog('TEST', 'test.log')
        fhdl = open('test.log', mode='r', encoding='utf-8')
        line = fhdl.readlines()[0]
        print(line)
        fhdl.close()
        os.remove('test.log')

        logstr = line.split()
        tsec = logstr.pop(4)
        assert (logstr == expected_logstr) and (float(tsec) < expected_maxtime)

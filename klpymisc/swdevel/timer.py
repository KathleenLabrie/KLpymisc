"""
Time profiling tools.
"""
from __future__ import print_function

__author__ = 'Kathleen Labrie'

import time
from io import open

# pylint: disable=too-few-public-methods

class Timer(object):
    """
    The Timer wraps the code to be timed.  The timer starts when Timer
    is initiazed and ends when the block is exited.

    Parameters
    ----------
    verbose : boolean
        Print information to the screen.  Default False.

    Attributes
    ----------
    secs : float
        Number of seconds from entering to exiting.
    start : float
        Time in second when Timer was launched.
    end : float
        Time in second when Timer was stopped.

    Methods
    -------
    writelogs(name, logname)
        Write the results to a logfile on disk.  'name' simply identifies the
        block being times, to keep track of what's what.  'logname' is the
        name of the file to write to.

    Raises
    ------

    Notes
    -----
    Inspired from Huy Nguyen's guide to analyzing Python performance.
    www.huyng.com (2015)

    Examples
    --------
    from timer import Timer

    with Timer() as t:
        ...
        list of statements doing something
        ...
    t.writelog('block1', 'tprofile.log')
    """

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.start = None
        self.end = None
        self.secs = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.end = time.time()
        self.secs = self.end - self.start
        if self.verbose:
            print("elapse time: %f seconds" % self.secs)

    def writelog(self, name, logname):
        """
        Write the results to a logfile on disk.

        Parameters
        ----------
        name : string
            Identifies the block being times, to keep track of what's what.
        logname : string
            Name of the file to write the results to.

        Returns
        -------
        Raises
        ------
        Notes
        -----
        Examples
        --------
        """
        fhdl = open(logname, mode='a', encoding='utf-8')
        fhdl.write("Elapse time for " + name + ": " + str(self.secs) +
                   " secs\n")
        fhdl.close()


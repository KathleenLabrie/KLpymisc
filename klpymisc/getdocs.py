#!/usr/bin/env python
"""
Helper function to move the documentation to somewhere useful
like a 'share' directory.

Installing the documentation somewhere convenient
=================================================

The documentation is included in the egg, but it is not
really accessible.  The documentation is also in the source code
but you will probably want to delete that once you've installed
the module.

To extract the documentation and copy it somewhere useful, ::

   (from source code):
      klpymisc/getdocs.py /your/preferred/path
   (from installed egg):
      <where_egg_is_located>/klpymisc-0.1.0dev1-py2.7.egg/klpymisc/getdocs.py

will copy the documentation to /your/preferred/path/klpymisc.

"""

from pkg_resources import Requirement, resource_filename
import shutil
import os
import sys
import argparse

SHORT_DESCRIPTION = 'Install the documentation'

def parse_args(command_line_args):
    """
    Input arguments parser.

    Parameters
    ----------
    command_line_args : list
        List of input args from either the command line or another function.

    Returns
    -------
    An argparse Namespace object that contains the parsed inputs.
    """

    parser = argparse.ArgumentParser(prog='getdocs',
                                     description=SHORT_DESCRIPTION)
    parser.add_argument('destination', action='store', nargs=1,
                        type=str, default=None,
                        help='Where to put the docs')

    args = parser.parse_args(command_line_args)

    return args

def move_docs(destination):
    """
    Copy the documentation to a new destination

    Parameters
    ----------
    destination : str
        System path to the new destination.  The documentation will be
        copied to 'destination/share/klpymisc'
    """

    dirname = resource_filename(Requirement.parse('klpymisc'),
                            os.path.join('share', 'klpymisc'))
    sub_destination = os.path.join(destination, 'klpymisc')

    if os.path.isdir(os.path.join(sub_destination)):
        shutil.rmtree(os.path.join(sub_destination))
    shutil.copytree(dirname, sub_destination)

    return

def main(argv=None):
    """
    Command line access main function.
    Run with -h to get usage information.
    """

    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)

    move_docs(args.destination[0])

if __name__ == '__main__':
    sys.exit(main())





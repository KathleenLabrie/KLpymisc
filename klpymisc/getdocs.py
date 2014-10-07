#!/usr/bin/env python

from pkg_resources import Requirement, resource_filename
import shutil
import os
import sys
import argparse

SHORT_DESCRIPTION = 'Install the documentation'

def parse_args(command_line_args):
    parser = argparse.ArgumentParser(prog='getdocs',
                                     description=SHORT_DESCRIPTION)
    parser.add_argument('destination', action='store', nargs=1,
                        type=str, default=None,
                        help='Where to put the docs')
    
    args = parser.parse_args(command_line_args)
    
    return args

def move_docs(destination):
    

    dirname = resource_filename(Requirement.parse('klpymisc'),
                            os.path.join('share', 'klpymisc'))    
    sub_destination = os.path.join(destination, 'klpymisc')

    if os.path.isdir(os.path.join(sub_destination)):
        shutil.rmtree(os.path.join(sub_destination))
    shutil.copytree(dirname, sub_destination)
        
    return

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    
    move_docs(args.destination[0])

if __name__ == '__main__':
    sys.exit(main())





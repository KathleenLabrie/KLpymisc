#!/usr/bin/env python

from __future__ import print_function

import sys
import argparse

import csv
from datetime import datetime
from dateutil import parser
# from datatime import date

VERSION = '1.0.0'

SHORT_DESCRIPTION = 'Convert app cvs to webtimesheet format'

def parse_args(command_line_args):
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description=SHORT_DESCRIPTION)
    parser.add_argument('inputfile', type=str,
                   help='CSV input file')

    args = parser.parse_args(command_line_args)

    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv

    args = parse_args(sys.argv[1:])

    table = csv.DictReader(open(args.inputfile))
    records = []
    for record in table:
        records.append(record)

    categories = []
    for record in records:
        category = record[' Tag']
        if category not in categories:
            categories.append(category)

    # today = date.today()
    # firstday = today
    # for record in records:
    #    starttime = record[' Start time']
    #    the_date = \
    #            datetime.strptime(starttime, "%b %d, %Y, %H:%M:%S %Z").date()
    #    if the_date < firstday:
    #        firstday = the_date


    timecard = {}
    for category in categories:
        timecard[category] = {}

    # timecard = { category1 : {date1 : total_duration,
    #                           date2 : total_duration,
    #                          },
    #            }

    for record in records:
        category = record[' Tag']
        the_date = parser.parse(record[' Start time']).date()
        # the_date = datetime.strptime(record[' Start time'], \
        #                             "%b %d, %Y, %H:%M:%S %Z").date()
        duration = float(record['Duration in hours'])
        if the_date in timecard[category]:
            timecard[category][the_date] += duration
        else:
            timecard[category][the_date] = duration

    for category in timecard.keys():
        print(category)
        for the_date in sorted(timecard[category].keys()):
            print('   ', the_date, timecard[category][the_date])


if __name__ == '__main__':
    sys.exit(main())

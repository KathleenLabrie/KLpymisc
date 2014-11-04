#!/usr/bin/env python

import sys
import argparse

import csv
from datetime import date, datetime

VERSION = '1.0.0'

SHORT_DESCRIPTION = 'Convert app cvs to webtimesheet format'

def load_records(inputfile):
    records = []


def parse_args(command_line_args):
    """
    Parse command line arguments.
    """
    
    p = argparse.ArgumentParser(description=SHORT_DESCRIPTION)
    p.add_argument('inputfile', type=str,
                   help='CSV input file')
    
    args = p.parse_args(command_line_args)
    
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
        category = record[' Category']
        if category not in categories:
            categories.append(category)
    
    #today = date.today()
    #firstday = today
    #for record in records:
    #    starttime = record[' Start time']
    #    date = datetime.strptime(starttime, "%b %d, %Y, %H:%M:%S %Z").date()
    #    if date < firstday:
    #        firstday = date
    
        
    timecard = {}
    for category in categories:
        timecard[category] = {}
    
    # timecard = { category1 : {date1 : total_duration,
    #                           date2 : total_duration,
    #                          },
    #            }
    
    for record in records:
        category = record[' Category']
        date = datetime.strptime(record[' Start time'], "%b %d, %Y, %H:%M:%S %Z").date()
        duration = float(record['Duration in hours'])
        if timecard[category].has_key(date):
            timecard[category][date] += duration
        else:
            timecard[category][date] = duration
    
    for category in timecard.keys():
        print category
        for date in sorted(timecard[category].keys()):
            print '   ', date, timecard[category][date]
    
    
if __name__ == '__main__':
    sys.exit(main())
    
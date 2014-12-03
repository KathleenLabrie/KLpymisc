#!/usr/bin/env python

import sys
import argparse

import csv
import re
from datetime import date, datetime, timedelta
import calendar

VERSION = '1.0.0'

COMPAT = 'CSV from OmniPlan 2.3.5'

SHORT_DESCRIPTION = 'Calculate monthly resource allocation from CSV export from OmniPlan'


def load_records(inputfile):
    records = []
    with open(inputfile, 'rb') as f:
        reader = csv.reader(f)
        try:
            firstrow = True
            for row in reader:
                if firstrow:
                    header = row
                    firstrow = False
                else:
                    records.append(TaskRecord(header, row))
        except csv.Error as e:
            sys.exit('File %s, line %d: %s' % (inputfile, reader.line_num, e))
    return records

def calculate_allocation(records):
    allocations = {}   # resource, AllocRecord
    for record in records:
        if len(record.record['Assigned']):
            # Parse the values obtained from the CSV.
            resources = parse_assigned(record.record['Assigned'])
            
            # First make sure theres a AllocRecord for each resource
            # in allocations dictionary.
            for (name, frac) in resources:
                if name not in allocations:
                    allocations[name] = AllocRecord(name)
            
            # Now, if there are multiple assignee to this task, the effort
            # must be split between the assigned based on the fractional
            # assignment.  
            
            effort_hours = parse_effort(record.record['Effort'])
            start_date = parse_date(record.record['Start'])
            end_date = parse_date(record.record['End'])
            
            # Now, calculate the effort per month
            if start_date.month == end_date.month:
                # Effort contained within one month.
                month = date(start_date.year, start_date.month, 1)
                for (name, frac) in resources:
                    allocations[name].add_effort(month, effort_hours * frac)
            else:
                # Effort spread over multiple months
                
                # Effort in partial months (first and last)
                ndays = abs(end_date - start_date).days + 1
                effort_per_day = effort_hours / ndays
                days_in_first = calendar.monthrange(start_date.year, 
                                                    start_date.month)[1] \
                                - start_date.day + 1
                days_in_last = end_date.day
                first_month = date(start_date.year, start_date.month, 1)
                last_month = date(end_date.year, end_date.month, 1)
                for (name, frac) in resources:
                    allocations[name].add_effort(first_month, 
                                     effort_per_day * days_in_first * frac)
                    allocations[name].add_effort(last_month,
                                     effort_per_day * days_in_last * frac)
                
                # For the months in between...
                list_of_months = monthly(start_date, end_date, 
                                         include_limits=False)
                for month in list_of_months:
                    days = calendar.monthrange(month.year, month.month)[1]
                    for (name, frac) in resources:
                        allocations[name].add_effort(month, 
                                                effort_per_day * days * frac)
                    
        else:
            # If the task is not assigned, skip.  eg. milestones, group tasks.
            continue        
    
    return allocations

def write_allocations(allocations, outputfile):
    # Find the period to report.  Find first and last month of all allocations.
    earliest = date(2100,1,1)
    latest = date(2000,1,1)
    for resource in allocations:
        e = allocations[resource].first_month()
        l = allocations[resource].last_month()
        if e < earliest:
            earliest = e
        if l > latest:
            latest = l

    # Create header: Resource Month1 Month2 MonthN
    header = ['Resource']
    list_of_months = monthly(earliest, latest)
    for month in list_of_months:
        header.append(month.strftime("%B%Y"))
    
    # For each allocation, create row, use ordered datetime.date
    alloc_rows = []
    for resource in sorted(allocations.keys()):
        row = []
        row.append(allocations[resource].resource)
        for month in list_of_months:
            if month in allocations[resource].allocation:
                row.append('%f' % (allocations[resource].allocation[month]))
            else:
                row.append('0.')
        alloc_rows.append(row)
                
    with open(outputfile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(alloc_rows)
    return

#------------------------------------------------------------------
# Classes

class TaskRecord:
    def __init__(self, header, row):
        self.record = dict(zip(header, row))

class AllocRecord:
    def __init__(self, resource):
        self.resource = resource
        self.allocation = {}  #key on datetime.date tuple for month_year
    
    def add_effort(self, month, effort):
        # add effort to a month record in allocation
        # month is a datetime.date set on first day of the month
        if month in self.allocation:
            self.allocation[month] += effort
        else:
            self.allocation[month] = effort

        
    def first_month(self):
        # find first month in allocation dict
        earliest = date(2100,1,1)
        for key in self.allocation:
            if key < earliest:
                earliest = key
        return earliest
    
    def last_month(self):
        # find last month in allocation dict
        latest = date(2000,1,1)
        for key in self.allocation:
            if key > latest:
                latest = key
        return latest


#------------------------------------------------------------------
# Utility functions

def monthly(start, end, include_limits=True):
    one_month = timedelta(calendar.monthrange(start.year, start.month)[1])
    if include_limits:
        d = date(start.year, start.month, 1)
    else:
        d = start + one_month
        d = date(d.year, d.month, 1)
    
    list_of_months = []
    
    while d < end and abs(end - d) >= one_month:
        list_of_months.append(d)
        one_month = timedelta(calendar.monthrange(d.year, d.month)[1])
        d = d + one_month
        d = date(d.year, d.month, 1)
        one_month = timedelta(calendar.monthrange(d.year, d.month)[1])
    
    if include_limits:
        list_of_months.append(d)

    return list_of_months

def parse_assigned(assigned_string):
    # There might be multiple assignee.  Those are separated with ';'
    assigned_resources = assigned_string.split(';')
    
    # separate the allocation fraction information from the name.
    resources = []
    total_fraction = 0.
    for assignee in assigned_resources:
        (name, fracstring) = assignee.split('{',1)
        name = name.rstrip().lstrip()
        f_of_f = re.search('(\d+)\% of (\d+)\%', fracstring).groups()
        fraction = float(f_of_f[0])*float(f_of_f[1]) / 10000.
        total_fraction += fraction
        resources.append([name, fraction])
    # fraction is global, but we want fraction of this task only
    for resource in resources:
        resource[1] = resource[1]/total_fraction
        
    return resources

def parse_effort(effort_string):
    multiplicator = { 'mo' : 160.,
                    'w'  : 40.,
                    'd'  : 8.,
                    'h'  : 1.,
                    'm'  : 1/60.,
                    's'  : 1/3600
                   }
    effort_list = effort_string.split()
    effort = 0.
    for time_str in effort_list:
        (effort_str, mult_id) = re.split('([a-z]+)', time_str)[:2]
        effort += float(effort_str) * multiplicator[mult_id]
    return effort

def parse_date(date_string):
    date_only = date_string.split()[0]
    date = datetime.strptime(date_only, "%m/%d/%y").date()    
    return date

#------------------------------------------------------------------
# Command-line handling

def parse_args(command_line_args):
    """
    Parse command line arguments.
    """
    p = argparse.ArgumentParser(description=SHORT_DESCRIPTION)
    p.add_argument('inputfile', type=str,
                   help='CSV input file')
    p.add_argument('outputfile', type=str,
                   help='CSV output file')
    p.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   default=False,
                   help='Toggle verbose on')
    p.add_argument('--debug', dest='debug', action='store_true', 
                   default=False,
                   help='Toggle debug on')
    
    args = p.parse_args(command_line_args)
    
    if args.debug:
        print args
    
    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    args = parse_args(sys.argv[1:])
    
    records = load_records(args.inputfile)
    if args.debug:
        for record in records:
            print record.record['Assigned'], record.record['Effort']
            
    allocations = calculate_allocation(records)
    if args.debug:
        for resource in sorted(allocations.keys()):
            print allocations[resource].resource
            for month in allocations[resource].allocation:
                print '   ', month.strftime("%B%Y"), allocations[resource].allocation[month]
                
    write_allocations(allocations, args.outputfile)

if __name__ == '__main__':
    sys.exit(main())
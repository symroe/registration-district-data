#!/usr/bin/env python3

# map Registration District CSV to register-style TSV

import sys
import csv
import re

sep = '\t'

fields = [
    'name',
    'start-date',
    'end-date',
]

maps = {
    '1837': 'Sept 1837 to 1851',
    '1852': '1852 to June 1946',
    '1946': 'Sept 1946 to March 1965',
    '1965': 'June 1965 to March 1974',
    '1974': 'June 1974 to Dec 1992',
    '1993': 'Mar 1993 to Dec 1996',
    '1997': '1997 to 2001'
}

notes = ['abolished']

fieldnames = fields + sorted(list(maps.keys())) + notes

rows = []

def n7e(code):
    if code.startswith("CREATED") or code.startswith("ABOLISHED"):
        return ""

    if code.startswith("*"):
        return ""

    return code


def find_code(row):
    code = row['1997 to 2001']

    return n7e(code)


def find_date(row, prefix):
    for field in row:
        if row[field].startswith(prefix):
            return re.sub("\D", "", row[field])
    return ""


def abolished(row):
    note = row['1997 to 2001']
    if not note.startswith('*'):
        return ""

    # fix broken note references
    if not note.endswith('*'):
        note = note + "*"

    return note


print(sep.join(fieldnames))

reader = csv.DictReader(sys.stdin, delimiter=sep)

for row in reader:

    row['name'] = row['Registration District']
    row['start-date'] = find_date(row, 'CREATED')
    row['end-date'] = find_date(row, 'ABOLISHED')
    row['abolished'] = abolished(row)

    for m in maps:
        row[m] = n7e(row[maps[m]])
        if row[m] == '-':
            row[m] = ''

    rows.append(row)

for row in sorted(rows, key=lambda row: row['name']):
    print(sep.join([row[field] for field in fieldnames]))

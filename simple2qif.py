#!/usr/bin/env python
import re
import csv
import argparse
from datetime import datetime, date

parser = argparse.ArgumentParser(description='Converts Simple.com CSV to QIF')
parser.add_argument("csvfile", type=argparse.FileType('r'))
args = parser.parse_args()

reader = csv.DictReader(args.csvfile)

match = re.search('^\d\d\d\d-\d\d-\d\d', args.csvfile.name)
qifname = 'simple-'
if match:
    qifname += match.group(0)
else:
    qifname += date.today().strftime('%Y-%m-%d')

def mkdate(csvdate):
    d = datetime.strptime(csvdate, '%Y/%m/%d')
    return d.strftime('%m/%d/%Y')

def writeQIFLine(f, row):
    f.write('D%s\n' % mkdate(row['Date']))
    f.write('T%s\n' % row['Amount'])
    f.write('P%s\n' % row['Description'])

    if row['Street address']:
        f.write('A%s\n' % row['Street address'])

    if row['City'] or row['State']:
        s = '%s %s' % (row['City'], row['State'])
        f.write('A%s\n' % s.strip())

    if row['Zip']:
        f.write('A%s\n' % row['Zip'])

    f.write('L%s:%s\n' % (row['Category folder'], row['Category']))

    if row['Memo']:
        f.write('M%s\n' % row['Memo'])
    f.write('^\n')


qif = open(qifname+'.qif','w')
qif.write('!Type:Bank\n')
for record in reader:
    # Ignore 'Check Hold' and 'Check Hold Release' entries
    if record['Description'].startswith('Check Hold'):
        continue
    # Ignore "Pending payment' activity, these are usually upcoming
    # payments that haven't yet triggered.
    if record['Activity'] == 'Pending payment':
        continue
    writeQIFLine(qif, record)

qif.close

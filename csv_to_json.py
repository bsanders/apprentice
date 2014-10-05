#! /usr/bin/python2
__author__ = 'bsanders'

import os
import sys
import csv
import json

def csv_to_json(filename):
    '''
    :param filename: a string representing the filename of the csv file
    Given a csv file 'foo.csv', will generate a json formatted 'foo.json'
    '''
    # "context manager"  Filehandle will automatically close at the end of the scope.
    with open(filename) as inputfile:
        csv_dict = csv.DictReader(inputfile)
        # dumps() converts an object to a JSON formatted string
        json_data = json.dumps([row for row in csv_dict], indent = 4)
    # splitext() returns a tuple with the filename without suffix, and the suffix
    basename = os.path.splitext(filename)[0]
    with open(basename + ".json", 'w') as outputfile:
        outputfile.write(json_data)

# if the json data file doesn't exist, but the csv does, create it.
if not os.path.exists('spells.json'):
    if os.path.exists('spells.csv'):
        csv_to_json('spells.csv')
    else:
        sys.exit(1)


# Check if the user passed an argument or not.
# sys.argv is a list of strings representing command-line arguments
if len(sys.argv) > 1:
    # list of dictionaries
    QUASI_DB = json.load(open('spells.json'))

    spell_id = int(sys.argv[1])
    spell = QUASI_DB[spell_id]
    print type(spell)
    print spell['name'], ": ", spell['short_description']
else:
    print "Usage: {0} <id number in the database to lookup>".format(sys.argv[0])

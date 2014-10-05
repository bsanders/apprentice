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


def db_retrieve_spell(spell_id):
    '''
    :param spell_id: a string representing the database ID of the spell
    :return: a dictionary representing that spell, or None
    '''
    # list of dictionaries
    QUASI_DB = json.load(open('spells.json'))

    # loop through the "db" until we find the spell entry that matches the id to lookup
    for entry in QUASI_DB:
        if entry['id'] == spell_id:
            # if we found a match, no need to continue
            break
    else:
        # note this unique syntax.  'else' really should have been called 'nobreak' here...
        return None
    return entry

# if the json data file doesn't exist, but the csv does, create it.
if not os.path.exists('spells.json'):
    if os.path.exists('spells.csv'):
        csv_to_json('spells.csv')
    else:
        sys.exit(1)


# Check if the user passed an argument or not.
# sys.argv is a list of strings representing command-line arguments
if len(sys.argv) > 1:
    spell_id = sys.argv[1]
    spell = db_retrieve_spell(spell_id)
    # look at this.  'None' is 'falsey'
    print type(spell)
    if spell:
        print spell['name'], ": ", spell['short_description']
        sys.exit(0)
    else:
        print "Spell not found with id {0}".format(spell_id)
        sys.exit(1)
else:
    print "Usage: {0} <id number in the database to lookup>".format(sys.argv[0])
    sys.exit(1)

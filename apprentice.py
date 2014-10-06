#! /usr/bin/python2
__author__ = 'bsanders'

import os
import sys
import csv
import json

from flask import Flask, jsonify, abort

# We're creating a flask object from this script
# don't worry, its just boilerplate
app = Flask(__name__)

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
        # print the name of each spell as we search.
        print entry['name']
        if entry['id'] == spell_id:
            # if we found a match, no need to continue
            break
    else:
        # note this unique syntax.  'else' really should have been called 'nobreak' here...
        return None
    return entry


# This is a 'decorator'. A decorator is an object that takes a function as an argument
# and returns a new, modified, function
# This decorator 'route' is provided by flask.
@app.route('/spells/api/v1.0/spells/<string:spell_id>', methods = ['GET'])
def get_spells(spell_id):
    '''
    :param spell_id: a string representing the database ID of the spell
    :return: An http response with that spell's name and description, or a 404 Page
    '''
    spell_dict = db_retrieve_spell(spell_id)
    if not spell_dict:
        # The beloved 404 Not Found error...
        abort(404)
    # jsonify takes in a dictionary, and returns a JSON document bundled in an HTTP response
    return jsonify({
        'name': spell_dict['name'],
        'short_description': spell_dict['short_description']})


# Since we're starting the script from the command line, we need this line, too.
if __name__ == '__main__':
    # if the json data file doesn't exist, but the csv does, create it.
    if not os.path.exists('spells.json'):
        if os.path.exists('spells.csv'):
            csv_to_json('spells.csv')
        else:
            sys.exit(1)

    app.run(debug = True)

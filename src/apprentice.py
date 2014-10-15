#! /usr/bin/python2
__author__ = 'bsanders'

import os
import time
import json

from flask import Flask, jsonify, abort

import redis

DATA_FILE = "../data/spells.json"

# More boilerplate, really.  In fact, we could have left this as default args!
redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

# We're creating a flask object from this script
# don't worry, its just boilerplate
app = Flask(__name__)

# Let's centrally define the spell attributes we actually care about.
SPELL_ATTRIBUTES = [
    'name',
    'duration',
    'description',
    'short_description',
    'linktext',
    'source',
    ]


def db_retrieve_spell(spell_id):
    '''
    :param spell_id: a string representing the database ID of the spell
    :return: a dictionary representing that spell, or None
    '''
    # list of dictionaries
    QUASI_DB = json.load(open(DATA_FILE))
    # simulate a long database lookup
    time.sleep(5)

    spell_id = spell_id.lower().strip()
    # Determine if the user is doing a lookup by id number or spell name
    if spell_id.isdigit():
        key = "id"
    else:
        key = "name"

    # loop through the "db" until we find the spell entry that matches the id to lookup
    for entry in QUASI_DB:
        # print the name of each spell as we search.
        print "found: ", entry['name']
        if entry[key].lower() == spell_id:
            # if we found a match, no need to continue
            break
    else:
        # note this unique syntax.  'else' really should have been called 'nobreak' here...
        return None
    return entry


def cache_retrieve_spell(spell_id):
    '''
    :param spell_id: a string representing the database ID of the spell
    :return: a dictionary representing that spell, or None
    On a cache-miss, we grab the spell from the database, and add it to the cache.
    '''
    print spell_id
    # Determine if the user is doing a lookup by id number or spell name
    if spell_id.isdigit():
        query_string = "spell:id:"
    else:
        query_string = "spell:name:"

    # using redis (for this purpose) is really easy. get() returns a string or None
    spell_json = redis_db.get(query_string + spell_id.lower().strip()) # redis returns a JSON-string
    print "checking cache_retrieve() for: {0}".format(spell_id)

    # if it was in the cache, grab the JSON string and convert to a dict
    if spell_json:
        return json.loads(spell_json)
    # if it was in the cache but an invalid search, return None
    elif spell_json == '':
        return None

    # otherwise, lookup the spell in the DB
    spell_dict = db_retrieve_spell(spell_id)
    if spell_dict:
        # if found, convert to a string and add to the cache. store names lower()'d
        redis_db.set("spell:id:" + spell_dict['id'], json.dumps(spell_dict))
        redis_db.set("spell:name:" + spell_dict['name'].lower().strip(), json.dumps(spell_dict))
    else:
        # If we didn't find it, cache an empty string with an expiry time.
        # At least if we search again in the next hour, we'll not find it faster next time.
        redis_db.setex("spell:id:" + spell_id.lower().strip(), 60 * 60, '')
        redis_db.setex("spell:name:" + spell_id.lower().strip(), 60 * 60, '')
    # Regardless if found or None, return it
    return spell_dict


# This is a 'decorator'. A decorator is an object that takes a function as an argument
# and returns a new, modified, function
# This decorator 'route' is provided by flask.
@app.route('/spells/api/v1.0/spells/<string:spell_id>', methods = ['GET'])
def get_spells(spell_id):
    '''
    :param spell_id: a string representing the database ID of the spell
    :return: An http response with that spell's name and description, or a 404 Page
    '''
    spell_dict = cache_retrieve_spell(spell_id)
    if not spell_dict:
        # The beloved 404 "Not Found" error...
        abort(404)

    # We'll build a dictionary out of only the keys we care about using a dictionary comprehension
    data = {k: v for k, v in spell_dict.iteritems() if k in SPELL_ATTRIBUTES}

    # jsonify takes in a dictionary, and returns a JSON document bundled in an HTTP response
    return jsonify(data)


# Since we're starting the script from the command line, we need this line, too.
if __name__ == '__main__':
    # if the json data file doesn't exist, error out.
    if not os.path.exists(DATA_FILE):
        # 500 is a more appropriate error code -- "server error"
        abort(500)

    app.run(debug = True)


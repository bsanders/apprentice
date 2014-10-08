#! /usr/bin/python

import sys
import requests

protocol = "http://"
server = "localhost"
port = "5000"
spell_uri = "/spells/api/v1.0/spells/{0}"

if not port:
    URI = protocol + server + spell_uri
else:
    URI = protocol + server + ":" + port + spell_uri

def get_spell_info(spell_id):
    '''
    :param spell_id: a string representing the database ID of the spell
    :return: a dictionary with the result, or None
    '''
    req = requests.get(URI.format(spell_id))

    # '200' means the HTTP request completed successfully.
    if req.status_code == 200:
        # return the JSON data in the response as a dictionary
        return req.json()
    else:
        return None

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print "Fetching spell id {0}...".format(sys.argv[1])
        spell = get_spell_info(sys.argv[1])
        if spell:
            print spell['name'], ": ", spell['short_description']
            print "Duration: ", spell['duration']
            print spell['description']
            print spell['source'], ": ", spell['linktext']
            sys.exit(0)
        else:
            print "Spell not found."
            sys.exit(1)
    else:
        print "Specify a spell id"
        sys.exit(1)

An Python Flask application to serve open content from the Pathfinder RPG via a RESTful API.
=====================================================================

A project written at least partially to demonstrate how to architect a useful web app.  Apprentice comes with a Python CLI application to demonstrate consumption of the API as well.  The data files are provided as OGL content from Paizo, and are available in a separate repo on github: <https://github.com/bsanders/pathfinder_data>.  A proper WSGI script has not yet been written to run Apprentice.  Apprentice serves content as JSON for easy consumption.

#### Usage: ####
For testing:

./apprentice.py

To use the cli application, edit apprentice\_cli.py with the server details and then run:

./apprentice\_cli.py <spell\_name>

eg: 

./apprentice\_cli.py "magic missile"

#### Requirements: ####
* Python v2.4-2.7
* Apprentice also uses a REDIS server for caching.
* Apprentice also makes use of a number of third party Python modules, found in requirements.txt.


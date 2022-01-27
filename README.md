# demo-health

This repo contains the files used to generate the demo-health google sheet, that continuously monitors the health of our various demo environments in Klaviyo

# File structure

### `demo_checks.py`

this file takes in a store name and klaviyo private key as command-line argument, and uses it to run a bunch of checks, and write them to file

### `check_all.py`

this file contains a dictionary of store names mapped to klaviyo private key; it iterates through this dict to run `demo_checks.py` on each store

### `send_to_gsheets.py`

this file iterates through every .csv in directory and sends the data contained to a google sheet shared with the team

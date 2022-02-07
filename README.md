# Demo-Health

This repo contains the files used to generate the demo-health google sheet, that continuously monitors the health of our various demo environments in Klaviyo
Link to the Health Checklist: https://github.com/ninaephremidze/Klaviyo-E-commerce-Platform-Health-Checklist/blob/main/check_all.py

# File structure

### `demo_checks.py`

This file takes in a store name and klaviyo private key as command-line argument, and uses it to run a bunch of checks, and write them to file

### `check_all.py`

This file contains a dictionary of store names mapped to klaviyo private key; it iterates through this dict to run `demo_checks.py` on each store

### `send_to_gsheets.py`

This file iterates through every .csv in directory and sends the data contained to a google sheet shared with the team

### Helpful Reference Content

1. [Sample Google Sheet for Magento 2 health checklist:] (https://docs.google.com/spreadsheets/d/1G2l6RlGlp3BYN02-17O_keadPe3isYw0-j7_87iQ-YQ/edit#gid=50897110)

The final output is a table of data in Google Sheets
This is an illustrative example showcasing sample output for Magento 2

2. Google Sheets for various e-commerce platforms health checklist 
Depending on the ecommerce platform you are running, the output can vary slightly
This contains illustrative examples of output for other eCommerce platforms.

3. Instructions on how to enable the required Google APIs in the API Console  and how to use OAuth for web server applications.

4. Google API’s Client Library for Python

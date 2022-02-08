# Description:

This repo contains the files used to generate the demo-health google sheet, that continuously monitors the health of our various demo environments in Klaviyo
Link to the Health [Checklist:](https://github.com/ninaephremidze/Klaviyo-E-commerce-Platform-Health-Checklist/blob/main/check_all.py)

# File structure

### `demo_checks.py`

This file takes in a store name and klaviyo private key as command-line argument, and uses it to run a bunch of checks, and write them to file

### `check_all.py`

This file contains a dictionary of store names mapped to klaviyo private key; it iterates through this dict to run `demo_checks.py` on each store

### `send_to_gsheets.py`

This file iterates through every .csv in directory and sends the data contained to a google sheet shared with the team

### Helpful Reference Content

1. Sample Google Sheet for [Magento 2 health checklist:](https://docs.google.com/spreadsheets/d/1G2l6RlGlp3BYN02-17O_keadPe3isYw0-j7_87iQ-YQ/edit#gid=50897110)


The final output is a table of data in Google Sheets
This is an illustrative example showcasing sample output for Magento 2

2. [Google Sheets](https://docs.google.com/spreadsheets/d/19sF9aweqwn-wMyNQNrXqXCQIC1LTUuagXcsd3pYaruo/edit#gid=2094281381)for various e-commerce platforms health checklist
Depending on the ecommerce platform you are running, the output can vary slightly
This contains illustrative examples of output for other eCommerce platforms.

3. Instructions on how to enable the required Google APIs in the API Console  and how to use OAuth for [web server applications](https://developers.google.com/identity/protocols/oauth2/web-server#enable-apis)

4. Google API’s [Client Library for Python](https://github.com/googleapis/google-api-python-client/blob/cbb1f88b82b21f5cb9dcace33ffea3f95a189015/docs/client-secrets.md)


### What you need to run this doc:

1. Access to the source code on [Github](https://github.com/ninaephremidze/Klaviyo-E-commerce-Platform-Health-Checklist)
2. Environment to run the code (PyCharm, Replit, AWS, etc)
3. A blank Google Sheet you’ll use as the destination for data to be written 
4. Create a secret file for [google sheets credentials](https://developers.google.com/identity/protocols/oauth2/web-server#prerequisites)
5. Klaviyo account 

### How to Run The Code:

If you don’t have an environment setup, here are the possible alternatives on how to run the code in a serverless way:
1.[Run Serverless code via AWS Lambda](https://faun.pub/run-serverless-code-via-aws-lambda-e4f19efd3ed9)
2.[Use replit])https://replit.com/talk/ask/Running-a-program/15179), you can connect it to Github 
3. Use [Google Colab](https://colab.research.google.com/)

### Steps to run the code:

Step I:

You can use the [check_all.py](https://docs.google.com/document/d/1hCH_d5Hug6f3suWbriII0azIj3ohfFEJRRMytxv7J_w/edit#) or the [demo_checks.py](https://github.com/ninaephremidze/Klaviyo-E-commerce-Platform-Health-Checklist/blob/main/demo_checks.py) code to achieve your goal.

The main difference between them is that:

Running check_all.py will itself then run demo_checks.py for each store type, ex. Magento2, Shopify, Big Commerce, etc.
Comment out the stores you don’t want ( Shopify, WooCommerce)
Add your Klaviyo private key as the key to each store in the dictionary
Run the code


If you were to run the demo_checks.py, it will automatically run for each store.
This will get the data from Klaviyo and save it in your working folder directory as a store_name.csv for each store.

Step II:
Once you execute the above steps, you’d need to [send_to_gsheets.py](https://github.com/ninaephremidze/Klaviyo-E-commerce-Platform-Health-Checklist/blob/main/send_to_gsheets.py) will upload the csv files to google sheets
First, make sure you install the correct packages as shown in the send_to_gsheets.py, otherwise your code will be gray and it will not run.
pip install  correct packages
pip install google-api-python-client

In order for us to be able to upload the information we got from Klaviyo to google sheets, follow these steps:
[Open API library in Google API console](https://developers.google.com/api-client-library)
Search for Google Sheets API and click enable 
P.S. You may need to make a project, if you are on a managed google account and not personal
Create credentials, Google API, user data
Search for [scope](https://www.googleapis.com/auth/spreadsheets) and add it
In Google API console, select "desktop app"
Name it demo-health-master ( you can use any name)
Download your credentials (client_secrets.json)
Place the file in your folder and rename it to "credentials.json"
Add your email to list of test users in Google API console
Create a blank Google sheet
Copy the spreadsheet id into the code
Create a tab named correctly for each of your stores ( Magento 2)



Run the code→ 
Congrats! You should have the information generated in your google sheets










# To upload the data from the good_to_go_table in PostgreSQL to Salesforce, you'll need to use the Salesforce REST API to make HTTP requests to the Salesforce server. The Salesforce REST API allows you to create, read, update, and delete records in Salesforce.

# Here's a simple Python script that shows how to upload the data from the good_to_go_table in PostgreSQL to Salesforce:



# In this example, field1 and field2 are assumed to be the fields in the good_to_go_table and the corresponding fields in Salesforce. 
# You'll need to replace <instance_name>, <api_version>, and <object_name> with the appropriate values for your Salesforce instance. 
# Additionally, you'll need to replace os.getenv("SF_ACCESS_TOKEN") with the appropriate value for the access token
# that allows you to access the Salesforce REST API.

import psycopg2
import requests
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cursor = conn.cursor()

# Query the data from the good_to_go_table
cursor.execute("SELECT * FROM good_to_go_table")
records = cursor.fetchall()

# Prepare the headers for the HTTP request
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.getenv("SF_ACCESS_TOKEN")
}

# Iterate over the records and make HTTP requests to the Salesforce REST API
for record in records:
    payload = {
        "field1": record[0],
        "field2": record[1],
        # ...
    }
    response = requests.post("https://<instance_name>.salesforce.com/services/data/v<api_version>/sobjects/<object_name>", headers=headers, json=payload)
    if response.status_code == 201:
        print("Record created successfully")
    else:
        print("Failed to create record:", response.text)

# Close the connection
conn.close()

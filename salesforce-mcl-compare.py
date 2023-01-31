
# Pull in Information from Salesforce and csv and compare

import os
import requests
import psycopg2
import json
import dotenv
import csv

# Load the environment variables from the .env file
dotenv.load_dotenv()

# Get the environment variables from the .env file
instance_url = os.getenv("SALESFORCE_INSTANCE_URL")
access_token = os.getenv("SALESFORCE_ACCESS_TOKEN")
object_api_name = os.getenv("SALESFORCE_OBJECT_API_NAME")
database_host = os.getenv("DATABASE_HOST")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=database_host,
    database=database_name,
    user=database_user,
    password=database_password
)

# Define the query to extract data from Salesforce
query = "SELECT Id, Name, Your_Matching_Field FROM " + object_api_name

# Make a GET request to the Salesforce REST API to execute the query
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}
url = instance_url + "/services/data/v49.0/query/?q=" + query
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    raise Exception("Failed to execute query. Response status code: " + str(response.status_code))

# Parse the response to a Python dictionary
records = json.loads(response.text)["records"]

# Open the CSV file
# Assumes CSV is in the same directory as script, if not use a relative path
with open("input.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader) # skip header row
    for row in reader:
        csv_field = row[0] # assuming the matching field is in the first column of the CSV file
        match = False
        for record in records:
            if record["Your_Matching_Field"] == csv_field:
                match = True
                break

        # Perform actions based on the result of the match
        if match:
            # Perform actions if the match is found
            pass
        else:
            # Perform actions if the match is not found
            pass

conn.commit()
conn.close()

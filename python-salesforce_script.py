import os
import requests
import psycopg2
import json
import dotenv

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
query = "SELECT Id, Name FROM " + object_api_name

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

# Insert the records into the PostgreSQL database
with conn.cursor() as cursor:
    for record in records:
        cursor.execute("INSERT INTO salesforce_records (id, name) VALUES (%s, %s)", (record["Id"], record["Name"]))

conn.commit()
conn.close()

# In the script, replace the placeholders (e.g. yourInstance.salesforce.com) with your specific 
# Salesforce instance URL, access token, object API name, and PostgreSQL database connection details. 
# The script assumes that you have created a table in your PostgreSQL database named salesforce_records with columns id and name.
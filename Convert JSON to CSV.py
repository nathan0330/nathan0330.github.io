#------------------------------------------------------------------#

## Import all modules that needed ##

import pandas as pd   #----- Import Pandas package
import os               #----- lets your code talk to the operating system such as file paths, directories, and environment variables.
import json           # Coverts JSON text to python dict and list
import glob           # finding files that match pattern
from azure.storage.blob import BlobServiceClient    # connect to azure server
from datetime import datetime    # date and time for python

#-------------------------------------------------------------#

## Set folder path where the JSON file gets dropped weekly ##

path = '/Users/nathanhan/Desktop/Data Engineering/Project/Car Failure Data Json'


#-------------------------------------------------------------#

## Crate a function that reads the latest file from the path and return as a JSON file. ##

def read_json(file_path):
    # Find all JSON files in the folder.
    files = glob.glob(os.path.join(file_path, "*.json"))

    # Pick the most recently modified file.
    newest_file = max(files, key=os.path.getmtime)

    # turns the file into a python object(dict or a list)
    with open(newest_file) as f:
        data = json.load(f)
    return data

#-------------------------------------------------------------#

## Convert object to a csv file ##

def json_to_csv(data):

    # store data in items and convert to a dataframe(row colum based format)
    items = data["rows"]
    df = pd.DataFrame(items)

    # Add new column week and give a date across all columns(date == the week the data was updated)
    df["Week"] = data["generated"]

    # Convert dataframe to CSV file and save to local drive & passes on
    df.to_csv(os.path.join('/Users/nathanhan/Desktop/Data Engineering/Project/Car Failure Data CSV', f"failure-mileage-distribution-{datetime.now():%Y-%m-%d}.csv"), index=False)
    print("Successfully saved failure-mileage-distribution.csv")
    return df.to_csv(index=False)

#-------------------------------------------------------------#

# store azure connection string.
connection_string = "replce with Azure_connection_key_"

## upload csv file to azure storage ##

def upload_csv_to_azure(csv_data):

    # Set container name (where the file is being dropped) & set file name
    container_name = "failure-mileage-distribution-project"
    blob_name = f"CSV_Files/failure-mileage-distribution-{datetime.now():%Y-%m-%d}.csv"

    #connect to the whole Azure storage account (like logging into the drive)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    #write the destination address: this container + this exact file name — nothing sent yet
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)

    # actually send csv_data to that address; overwrite=True replaces it if a file is already there
    blob_client.upload_blob(csv_data, overwrite=True)

    print(f"Successfully uploaded {blob_name} to {container_name}")

#-------------------------------------------------------------#
failure_file = read_json(path)
csv = json_to_csv(failure_file)
upload_csv_to_azure(csv)



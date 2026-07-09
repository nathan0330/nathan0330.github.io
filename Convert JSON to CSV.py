import requests
import pandas as pd
import os
import json
import glob

path = '/Users/nathanhan/Desktop/Data Engineering/Project/Car Failure Data Json'

def read_json(file_path):
    # Find all JSON files in the folder
    files = glob.glob(os.path.join(file_path, "*.json"))

    # Pick the most recently modified one
    newest_file = max(files, key=os.path.getmtime)

    with open(newest_file) as f:
        json_file = json.load(f)
    return json_file

def json_to_csv(file):
    items = file["rows"]
    df = pd.DataFrame(items)
    df["Week"] = file["generated"]
    df.to_csv(os.path.join('/Users/nathanhan/Desktop/Data Engineering/Project/Car Failure Data CSV', "failure-mileage-distribution.csv"), index=False)
    print("Successfully saved failure-mileage-distribution.csv")

failure_file = read_json(path)
json_to_csv(failure_file)



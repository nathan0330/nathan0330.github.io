import requests
import pandas as pd
import os
import json

path = "/Users/nathanhan/Desktop/failure-mileage-distribution.json"

def read_json(file_path):
    with open(file_path) as f:
        json_file = json.load(f)
    return json_file

def json_to_csv(file):
    items = file["rows"]
    df = pd.DataFrame(items)
    df.to_csv(os.path.join("/Users/nathanhan/Desktop", "failure-mileage-distribution.csv"), index=False)
    print("Successfully saved failure-mileage-distribution.csv")



failure_file = read_json(path)
json_to_csv(failure_file)




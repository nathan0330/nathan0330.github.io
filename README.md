# Auto Vehicle Failure-Mileage Distribution Data Pipeline
-------here goes the description of the pipeline-------
       where the data was downloaded, stored, cleaning process, any trnasformation!

## 1.Data Source
The Failure-Mileage Distribution dataset build from NHTSA (Nattional Highway Traffic Safety Association) owner complaint and recall record.
Dataset consist of data NHTSA reporting auto failure based on year, model, make, cateoetegoy and provideds odometer milage at failure.
Note that not all failure report reports the failure milage as it is option to report the odometer milage base on reporter preference. 
This means that there will be a difference between the total complaint count vs sample size used to measue the average.

### Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| `year` | int | Vehicle model year |
| `make` | string | Manufacturer |
| `model` | string | Model |
| `component` | string | Failure category (NHTSA component taxonomy) |
| `complaints` | int | Total NHTSA complaints in this cluster |
| `mileage_samples` | int | Complaints carrying a valid odometer reading — basis for the percentiles |
| `mileage_p25` | int | 25th-percentile failure mileage |
| `mileage_median` | int | Median failure mileage |
| `mileage_p75` | int | 75th-percentile failure mileage |
| `est_repair_usd` | int | Estimated independent-shop repair cost (USD) |
| `severity` | string | Failure severity: critical \| severe \| moderate |
| `url` | string | Source page on ProblemsByVin |



## 2. Convert JSON file to CSV & Upload to ADLS 


Once the weekly JSON export is dropped into the source folder, the pipeline picks it up, transforms it into a clean tabular format, and loads it into Azure storage. This is handled by three Python functions working together: read_json, json_to_csv, and upload_csv_to_azure.

### 2.1 Reading the Latest JSON File

```python
def read_json(file_path):
    # Find all JSON files in the folder.
    files = glob.glob(os.path.join(file_path, "*.json"))

    # Pick the most recently modified file.
    newest_file = max(files, key=os.path.getmtime)

    # turns the file into a python object(dict or a list)
    with open(newest_file) as f:
        data = json.load(f)
    return data
```
Rather than hardcoding a specific filename, this function scans the source folder for all .json files and automatically selects the most recently modified one. This allows new weekly exports to be dropped into the folder without requiring any changes to the script. The file is then parsed from raw JSON text into a Python dictionary, ready for transformation.

### 2.2 Converting JSON to CSV
```python
def json_to_csv(data):

    # store data in items and convert to a dataframe(row colum based format)
    items = data["rows"]
    df = pd.DataFrame(items)

    # Add new column week and give a date across all columns(date == the week the data was updated)
    df["Week"] = data["generated"]

    # Convert dataframe to CSV file and save to local drive & passes on
    df.to_csv(os.path.join('File_Path_Goes_here', f"failure-mileage-distribution-{data['generated']}.csv"), index=False)
    print("Successfully saved failure-mileage-distribution.csv")
    return df.to_csv(index=False)
```
The row-level data is loaded into a pandas DataFrame, giving it a structured, tabular shape. Every row is tagged with a Week column derived from the JSON's generated field, ensuring each weekly batch is traceable to the period it represents. A local CSV copy is saved for backup/auditing purposes, using the same generated date in the filename to keep local files and cloud uploads consistently named. The function also returns the CSV content as an in-memory string, so it can be passed directly to the upload step without needing to reopen the saved file.

### 2.3 Uploading to Azure Storage
```python
def upload_csv_to_azure(csv_data, data):

    # Set container name (where the file is being dropped) & set file name
    container_name = "failure-mileage-distribution-project"
    blob_name = f"CSV_Files/failure-mileage-distribution-{data['generated']}.csv"

    #connect to the whole Azure storage account (like logging into the drive)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    #write the destination address: this container + this exact file name — nothing sent yet
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)

    # actually send csv_data to that address; overwrite=True replaces it if a file is already there
    blob_client.upload_blob(csv_data, overwrite=True)

    print(f"Successfully uploaded {blob_name} to {container_name}")
```
The CSV content is uploaded to Azure Blob Storage using the azure-storage-blob SDK. The upload targets a dated blob name (matching the local file), landing in a dedicated folder within the storage container. Using the generated date rather than the upload timestamp ensures each week's file is stored under a unique, meaningful name — preventing accidental overwrites and preserving a full historical record of weekly snapshots.

### 2.4 End-to-End Execution
```python
auto_failure_weekly_json_file = read_json(path)
auto_failure_weekly_csv_file = json_to_csv(auto_failure_weekly_json_file)
upload_csv_to_azure(auto_failure_weekly_csv_file, auto_failure_weekly_json_file)
```
These three steps run sequentially: the newest JSON file is located and loaded, transformed into CSV format, and uploaded to cloud storage — completing the ingestion process for that week's data.

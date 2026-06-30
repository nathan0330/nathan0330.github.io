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



download JSON file from website convert to csv file

Use the Convert JSON to CSV.py code file to convert the JSON file to a CSV.



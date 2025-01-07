# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "063cd542-02d5-4b5a-82dd-91ae40082019",
# META       "default_lakehouse_name": "LH_Bronze",
# META       "default_lakehouse_workspace_id": "eeea7f95-5551-4edd-b0f8-580c5f0cf215"
# META     }
# META   }
# META }

# PARAMETERS CELL ********************

# Parameters (Passed in by your pipeline)
__API_URL =   "https://jsonplaceholder.typicode.com/"
__DATA_ENTITY = "posts"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Import necessary libraries
from pyspark.sql.functions import col, explode, lit
import requests
import json

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Function to fetch data from the API
def fetch_data(__API_URL):
    try:
        response = requests.get(__API_URL)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Fetch data from the API
data = fetch_data(__API_URL + __DATA_ENTITY)

# Check if data was fetched successfully
if data:
    # Convert data to Spark DataFrame
    df = spark.read.json(spark.sparkContext.parallelize([json.dumps(data)]))

    # If the data is nested, you may want to explode or flatten it
    if isinstance(data, list) and isinstance(data[0], dict):
        df = df.select(*[col(f"{c}") for c in df.columns])

    # Add metadata column (e.g., data entity type)
    df = df.withColumn("DATA_ENTITY", lit(__DATA_ENTITY))

    # Write the DataFrame to JSON
    output_path = f"Files/ingest/{__DATA_ENTITY}.json"
    df.coalesce(1).write.mode("overwrite").json(output_path)

    print(f"Data successfully written to {output_path}")

else:
    print("No data fetched from the API.")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

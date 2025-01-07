# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "e8db0bc1-73ba-464f-9fdd-60fc72109e31",
# META       "default_lakehouse_name": "LH_Silver",
# META       "default_lakehouse_workspace_id": "eeea7f95-5551-4edd-b0f8-580c5f0cf215",
# META       "known_lakehouses": []
# META     }
# META   }
# META }

# PARAMETERS CELL ********************

__BRONZE_SCHEMA = "restapi"
__BRONZE_TABLE = "users"
__SILVER_SCHEMA = "jsonplaceholder"
__SILVER_TABLE = "users"
__SILVER_TABLE_BK_COLUMNS = 'id'
__SILVER_TABLE_EXTRACT_COLUMNS = "*"
__SILVER_TABLE_EXCLUDE_COLUMNS = "address, company"  

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, lit
import sempy.fabric as fabric

# Enable automatic schema evolution
spark.sql("SET spark.databricks.delta.schema.autoMerge.enabled = true") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

fabric_workspace_name = notebookutils.runtime.context.get("currentWorkspaceName")
fabric_workspace_id = notebookutils.runtime.context.get("currentWorkspaceId")
default_lakehouse_id = notebookutils.runtime.context.get("defaultLakehouseId")
default_lakehouse_name = notebookutils.runtime.context.get("defaultLakehouseName")

# Change 'Silver' to 'Bronze' to find correspongind Bronze-objects
bronze_lakehouse_name = default_lakehouse_name.replace("Silver", "Bronze")
bronze_workspace_name = fabric_workspace_name.replace("Silver", "Bronze")


# Filter workspaces to find the Bronze-workspace
bronze_workspace = fabric.list_workspaces(filter=f"name eq '{bronze_workspace_name}'")

# Extract 'id' and 'name' into variables
if not bronze_workspace.empty:  # Check if any workspaces were found
    bronze_workspace_id = bronze_workspace.iloc[0]['Id']  # Extract the first workspace's ID
    bronze_workspace_name = bronze_workspace.iloc[0]['Name']  # Extract the first workspace's name
    bronze_lakehouse_id = notebookutils.lakehouse.get(name=bronze_lakehouse_name, workspaceId=bronze_workspace_id).id

    print(f"Bronze:")
    print(f"> Lakehouse: {bronze_lakehouse_name} - {bronze_lakehouse_id}")
    print(f"> Workspace ID: {bronze_workspace_id}")
    print(f"> Workspace Name: {bronze_workspace_name}")
    print(f"")
    print(f"Silver:")
    print(f"> Lakehouse: {default_lakehouse_name} - {default_lakehouse_id}")
    print(f"> Workspace ID: {fabric_workspace_id}")
    print(f"> Workspace Name: {fabric_workspace_name}")
    print(f"")
else:
    print("No workspace found with the specified name.")
    notebookutils.notebook.exit("No Bronze workspace found.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

__SILVER_TABLE_BK_COLUMNS = __SILVER_TABLE_BK_COLUMNS.replace('[', '').replace(']', '')
__SILVER_TABLE_BK_COLUMNS = ["`" + x.strip() + "`" for x in __SILVER_TABLE_BK_COLUMNS.split(',')]
print("Business key columns: " + ", ".join(__SILVER_TABLE_BK_COLUMNS))

__BRONZE_WORKSPACE_ID = bronze_workspace_id
__BRONZE_LAKEHOUSE_ID = bronze_lakehouse_id
__BRONZE_PATH = "abfss://{workspaceId}@onelake.dfs.fabric.microsoft.com/{lakehouseId}".format(workspaceId = __BRONZE_WORKSPACE_ID, lakehouseId = __BRONZE_LAKEHOUSE_ID)

__SILVER_LAKEHOUSE = default_lakehouse_name
__SILVER_TABLE_FULLY_QUALIFIED_NAME = "`{lakehouse}`.`{schema}`.`{table}`".format(lakehouse = __SILVER_LAKEHOUSE,  schema = __SILVER_SCHEMA, table = __SILVER_TABLE)

# Lowercase everything
__BRONZE_WORKSPACE_ID = __BRONZE_WORKSPACE_ID.lower()
__BRONZE_LAKEHOUSE_ID = __BRONZE_LAKEHOUSE_ID.lower()
__BRONZE_PATH = __BRONZE_PATH.lower()
__SILVER_LAKEHOUSE = __SILVER_LAKEHOUSE.lower()
__SILVER_TABLE_FULLY_QUALIFIED_NAME = __SILVER_TABLE_FULLY_QUALIFIED_NAME.lower()

print(f"Bronze:")
print(f"> Path: {__BRONZE_PATH}")
print(f"")
print(f"Silver:")
print(f"> Table: {__SILVER_TABLE_FULLY_QUALIFIED_NAME}")
print(f"> Business key column(s): {__SILVER_TABLE_BK_COLUMNS}")
print(f"> Extract column(s): {__SILVER_TABLE_EXTRACT_COLUMNS}")
print(f"> Exclude column(s): {__SILVER_TABLE_EXCLUDE_COLUMNS}")
print(f"")
print(f"Create silver schema `{__SILVER_SCHEMA}` if not exists")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{__SILVER_SCHEMA}`")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Load Bronze JSON data into a DataFrame
bronze_df = spark.read.json(__BRONZE_PATH + f"/Files/ingest/{__BRONZE_TABLE}.json")

# Select specific columns if defined
if __SILVER_TABLE_EXTRACT_COLUMNS:
    bronze_df = bronze_df.select(*__SILVER_TABLE_EXTRACT_COLUMNS)
    print(f'Extracted columns: {__SILVER_TABLE_EXTRACT_COLUMNS}')

# Drop excluded columns if defined
if __SILVER_TABLE_EXCLUDE_COLUMNS:
    # Create a new DataFrame by selecting only the columns to keep
    columns_to_keep = [col_name for col_name in bronze_df.columns if col_name not in __SILVER_TABLE_EXCLUDE_COLUMNS]
    bronze_df = bronze_df.select(*columns_to_keep)
    
    print(f'Dropped columns: {__SILVER_TABLE_EXCLUDE_COLUMNS}')
    print('Bronze schema:')
    print(bronze_df.schema)

# Check if the Silver table exists
if spark.catalog.tableExists(__SILVER_TABLE_FULLY_QUALIFIED_NAME):
    # Load existing Silver table
    silver_df = spark.table(__SILVER_TABLE_FULLY_QUALIFIED_NAME)

    # Join Bronze and Silver on Business Key columns
    join_condition = [bronze_df[bk] == silver_df[bk] for bk in __SILVER_TABLE_BK_COLUMNS]
    updated_rows = bronze_df.join(silver_df, join_condition, "left_anti")

    # Concatenate updated and new rows
    result_df = updated_rows.unionByName(silver_df)
else:
    # If the Silver table doesn't exist, treat all rows as new
    result_df = bronze_df

# Write updated data back to Silver table
result_df.write.mode("overwrite").format("delta").saveAsTable(__SILVER_TABLE_FULLY_QUALIFIED_NAME)

print(f"Data successfully updated in Silver table: {__SILVER_TABLE_FULLY_QUALIFIED_NAME}")

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

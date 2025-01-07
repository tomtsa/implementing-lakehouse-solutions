-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "db455ef8-4479-4fb1-84af-45043b893a78",
-- META       "default_lakehouse_name": "LH_Silver_Configuration",
-- META       "default_lakehouse_workspace_id": "eeea7f95-5551-4edd-b0f8-580c5f0cf215",
-- META       "known_lakehouses": []
-- META     }
-- META   }
-- META }

-- CELL ********************

--jsonplaceholder

CREATE SCHEMA IF NOT EXISTS jsonplaceholder;

DROP TABLE IF EXISTS jsonplaceholder.silver;

CREATE TABLE jsonplaceholder.silver
(
	IsActive boolean  ,
	Type string  ,
	BronzeSchema string  ,
	BronzeTable string  ,
	SilverSchema string  ,
	SilverTable string  ,
	BusinessKeyColumns string  ,
	ExtractColumns string  ,
	ExcludeColumns string  ,
	Tag string  
);


INSERT INTO jsonplaceholder.silver
VALUES (
    1, 'JSON-SCD1', 'jsonplaceholder', 'posts', 'jsonplaceholder', 'posts', 'Id', '*', '', 'jsonplaceholder'
)
,
(
    1, 'JSON-SCD1', 'jsonplaceholder', 'comments', 'jsonplaceholder', 'comments', 'Id', '*', '', 'jsonplaceholder'
),
(
    1, 'JSON-SCD1', 'jsonplaceholder', 'users', 'jsonplaceholder', 'users', 'Id', '*', 'address, company', 'jsonplaceholder'
)



-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

SELECT * FROM jsonplaceholder.silver

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************


-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "synapse_pyspark"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "07d53a8c-f5b9-4b3d-9382-bc1018944d37",
-- META       "default_lakehouse_name": "LH_Bronze_Configuration",
-- META       "default_lakehouse_workspace_id": "eeea7f95-5551-4edd-b0f8-580c5f0cf215",
-- META       "known_lakehouses": []
-- META     }
-- META   }
-- META }

-- CELL ********************

--restapi

CREATE SCHEMA IF NOT EXISTS restapi;

DROP TABLE IF EXISTS restapi.bronze;

CREATE TABLE restapi.bronze
(
	IsActive boolean ,
	URL string,
	Dataset string,
	Source string,
	Query string,
	Tag string
);

INSERT INTO restapi.bronze
VALUES 

(
    1, 'https://jsonplaceholder.typicode.com/','posts', 'jsonplaceholder', '', 'jsonplaceholder'
)
,
(
    1, 'https://jsonplaceholder.typicode.com/','comments', 'jsonplaceholder', '', 'jsonplaceholder'
)
,
(
    1, 'https://jsonplaceholder.typicode.com/','users', 'jsonplaceholder', '', 'jsonplaceholder'
)
-- ,
-- (
--     1, 'https://jsonplaceholder.typicode.com/','albums', 'jsonplaceholder', '', 'jsonplaceholder'
-- )

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "synapse_pyspark"
-- META }

-- CELL ********************

SELECT * FROM restapi.bronze

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

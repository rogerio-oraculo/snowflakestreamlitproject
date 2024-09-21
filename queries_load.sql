-- Tabela stop_and_search

CREATE TABLE IF NOT EXISTS "CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."table_stop_and_search" (
    type VARCHAR, 
    date TIMESTAMP_NTZ, 
    part_of_a_policing_operation VARCHAR, 
    policing_operation VARCHAR, 
    latitude NUMBER(38, 6), 
    longitude NUMBER(38, 6), 
    gender VARCHAR, 
    age_range VARCHAR, 
    self_defined_ethnicity VARCHAR, 
    officer_defined_ethnicity VARCHAR, 
    legislation VARCHAR, 
    object_of_search VARCHAR, 
    outcome VARCHAR, 
    outcome_linked_to_object_of_search BOOLEAN, 
    removal_of_more_than_just_outer_clothing BOOLEAN
);

CREATE OR REPLACE TEMP FILE FORMAT "CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."temp_file_format_stop_and_search"
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_DELIMITER = ','
    TRIM_SPACE = TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    REPLACE_INVALID_CHARACTERS = TRUE
    DATE_FORMAT = AUTO
    TIME_FORMAT = AUTO
    TIMESTAMP_FORMAT = AUTO;

COPY INTO "CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."table_stop_and_search" 
FROM (
    SELECT 
        $1 AS type, 
        $2 AS date, 
        $3 AS part_of_a_policing_operation, 
        $4 AS policing_operation, 
        $5 AS latitude, 
        $6 AS longitude, 
        $7 AS gender, 
        $8 AS age_range, 
        $9 AS self_defined_ethnicity, 
        $10 AS officer_defined_ethnicity, 
        $11 AS legislation, 
        $12 AS object_of_search, 
        $13 AS outcome, 
        $14 AS outcome_linked_to_object_of_search, 
        $15 AS removal_of_more_than_just_outer_clothing
    FROM '@"CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."CRIMES_IN_LONDON_STAGE"'
) 
FILES = ('2024-07-city-of-london-stop-and-search.csv') -- Aqui você passa o nome do arquivo CSV como parâmetro
FILE_FORMAT = '"CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."temp_file_format_stop_and_search"' 
ON_ERROR = CONTINUE;

SELECT * FROM CRIMES_IN_LONDON_DB.CRIMES_IN_LONDON_SCHEMA."table_stop_and_search";

-- Tabela table_street

CREATE TABLE IF NOT EXISTS "CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."table_street" ( 
    crime_id VARCHAR, 
    month VARCHAR, 
    reported_by VARCHAR, 
    falls_within VARCHAR, 
    longitude NUMBER(38, 6), 
    latitude NUMBER(38, 6), 
    location VARCHAR, 
    lsoa_code VARCHAR, 
    lsoa_name VARCHAR, 
    crime_type VARCHAR, 
    last_outcome_category VARCHAR, 
    context VARCHAR 
); 

CREATE TEMP FILE FORMAT "CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."temp_file_format_street"
	TYPE=CSV
    SKIP_HEADER=1
    FIELD_DELIMITER=','
    TRIM_SPACE=TRUE
    FIELD_OPTIONALLY_ENCLOSED_BY='"'
    REPLACE_INVALID_CHARACTERS=TRUE
    DATE_FORMAT=AUTO
    TIME_FORMAT=AUTO
    TIMESTAMP_FORMAT=AUTO; 

COPY INTO "CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."table_street" 
FROM (
    SELECT 
        $1 AS crime_id, 
        $2 AS month, 
        $3 AS reported_by, 
        $4 AS falls_within, 
        $5 AS longitude, 
        $6 AS latitude, 
        $7 AS location, 
        $8 AS lsoa_code, 
        $9 AS lsoa_name, 
        $10 AS crime_type, 
        $11 AS last_outcome_category, 
        $12 AS context
	FROM '@"CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."CRIMES_IN_LONDON_STAGE"'
) 
FILES = ('2024-07-city-of-london-street.csv') -- Aqui você passa o nome do arquivo CSV como parâmetro
FILE_FORMAT = '"CRIMES_IN_LONDON_DB"."CRIMES_IN_LONDON_SCHEMA"."temp_file_format_street"' 
ON_ERROR = CONTINUE;

SELECT * FROM CRIMES_IN_LONDON_DB.CRIMES_IN_LONDON_SCHEMA."table_street";


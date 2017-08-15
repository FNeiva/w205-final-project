-- ##########################################################################################
-- # Dengue Fever Prediction System
-- # W205 Summer 2017 Final Project
-- # Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
-- ##########################################################################################
-- # Data Layer: Data Lake Table Creation Script
-- #
-- # This is the third script in the pipeline, and in the data layer. This script creates
-- # the Hive tables used for visualization and analysis later in the pipeline.
-- #
-- ##########################################################################################

-- Drop possible pre-existing old tables before recreating

DROP TABLE dengai_original_data;

-- Create DengAI original data table
--
-- This table stores the original DengAI data

CREATE EXTERNAL TABLE dengai_original_data (
  city string,
  year string,
  week_of_year string,
  week_start_date string,
  veg_ne string,
  veg_nw string,
  veg_se string,
  veg_sw string,
  precip_mm string,
  air_temp_K string,
  avg_temp_K string,
  dew_point_temp string,
  max_temp_K string,
  min_temp_K string,
  precip_kg_m2 string,
  rel_hum_pct string,
  sat_precip_mm string,
  spec_hum_g_kg string,
  tdtr_K string,
  avg_temp_C string,
  station_diurn_temp_C string,
  station_max_temp_C string,
  station_min_temp_C string,
  station_precip_mm string,
  city_rep string,
  year_rep string,
  week_of_year_rep string,
  num_cases string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = '"',
  "escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/dengue_prediction/original_data/dengai_data.csv';


-- Create Dengue History data table
--
-- This table stores the transformed Dengue History data

CREATE TABLE dengue_history_data AS
    SELECT
      city,
      year,
      week_of_year,
      CAST(avg_temp_K AS DOUBLE) AS avg_temp_K,
      CAST(dew_point_temp AS DOUBLE) AS dew_point_temp,
      CAST(max_temp_K AS DOUBLE) AS max_temp_K,
      CAST(min_temp_K AS DOUBLE) AS min_temp_K,
      CAST(rel_hum_pct AS DOUBLE) AS rel_hum_pct,
      CAST(avg_temp_C AS DOUBLE) AS avg_temp_C,
      CAST(num_cases AS INT) AS num_cases
    FROM
      dengai_transf_data;

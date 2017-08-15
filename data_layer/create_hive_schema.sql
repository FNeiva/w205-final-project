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

DROP TABLE dengue_history_data;

-- Create Dengue History table
--
-- This table stores the historical dengue data

CREATE EXTERNAL TABLE dengue_history_data (
  city string,
  year string,
  week_of_year string,
  avg_temp_K string,
  dew_point_temp string,
  max_temp_K string,
  min_temp_K string,
  rel_hum_pct string,
  avg_temp_C string,
  num_cases string
)
STORED AS TEXTFILE
LOCATION '/user/w205/dengue_prediction/transformed_data/dengue_data';

#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Data Layer Initialization Script
#
# This is the super script that runs the entire Data Layer pipeline. It will:
#
#     * Download the required data
#     * Work the downloaded data and put it in the appropriate format
#     * Create the HDFS file structure and load the original data into HDFS
#     * Transform the data to be used by the other layers
#     * Store the transformed in HDFS
#     * Create the Hive/SparkSQL schema to access the data
#
##########################################################################################

# The following export fixes problems with PySpark not finding the native Hadoop library
LD_LIBRARY_PATH=/opt/jdk1.7.0_79/jre/lib/amd64/server/:/usr/lib/hadoop/lib/native/
export LD_LIBRARY_PATH

echo "##########################################################"
echo "Dengue Fever Prediction System"
echo "Data Layer Initialization and Update Script"
echo "##########################################################"
echo " "
echo "This script will now initialize or update the Data Layer."
echo "It will run other scripts to download, transform and store the required data."
echo "This will probably take a few minutes, so please wait until it is finished."
echo " "
echo " "
echo "Step 1 of 3: Running Data Layer Loading Script... "
echo " "
echo " "
./data_layer/load_data_lake.sh
echo " "
echo "Step 1 of 3 done."
echo " "
echo "Step 2 of 3: Running Data Layer Transformation Script... "
echo " "
echo " "
/data/spark15/bin/spark-submit --packages com.databricks:spark-csv_2.10:1.5.0 ./data_layer/transform_data.py
echo " "
echo "Step 2 of 3 done."
echo " "
echo "Step 3 of 3: Creating Hive/SparkSQL schema... "
echo " "
echo " "
/data/spark15/bin/spark-sql -f ./data_layer/create_schema.sql
echo " "
echo "Step 3 of 3 done."
echo " "
echo "Data Layer Initialization and Update Script Finished!"

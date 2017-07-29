#!/bin/bash

# This script loads all the Hospital Compare files into the HDFS data lake for analysis

# Set temporary directory for extracting raw data files from the zip file
TMP_DIR=/data/tmp_ex1

# Remove old temporary directory if exists and then recreate
if [ -d $TMP_DIR ] ; then
	rm -r $TMP_DIR
fi
mkdir $TMP_DIR

# Download the file to the temporary directory
wget -O $TMP_DIR/hospitaldata.zip "https://data.medicare.gov/views/bg9k-emty/files/Nqcy71p9Ss2RSBWDmP77H1DQXcyacr2khotGbDHHW_s?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"

# Unzip the file in the temporary directory
unzip $TMP_DIR/hospitaldata.zip -d $TMP_DIR

# Strip the first line and rename the files we are interested in
tail -n +2 $TMP_DIR/"Hospital General Information.csv" > $TMP_DIR/hospitals.csv
tail -n +2 $TMP_DIR/"Timely and Effective Care - Hospital.csv" > $TMP_DIR/effective_care.csv
tail -n +2 $TMP_DIR/"Readmissions and Deaths - Hospital.csv" > $TMP_DIR/readmissions.csv
tail -n +2 $TMP_DIR/"Measure Dates.csv" > $TMP_DIR/measures.csv
tail -n +2 $TMP_DIR/"hvbp_hcahps_05_28_2015.csv" > $TMP_DIR/survey_responses.csv

# Clean existing directories and files in HDFS to remove possible old files
hdfs dfs -rm -r "/user/w205/hospital_compare"

# Recreate directory structure in the HDFS data lake
hdfs dfs -mkdir "/user/w205/hospital_compare"
hdfs dfs -mkdir "/user/w205/hospital_compare/hospitals"
hdfs dfs -mkdir "/user/w205/hospital_compare/effective_care"
hdfs dfs -mkdir "/user/w205/hospital_compare/readmissions"
hdfs dfs -mkdir "/user/w205/hospital_compare/measures"
hdfs dfs -mkdir "/user/w205/hospital_compare/survey_responses"

# Load files into the HDFS data lake directory structure
hdfs dfs -put $TMP_DIR/hospitals.csv "/user/w205/hospital_compare/hospitals"
hdfs dfs -put $TMP_DIR/effective_care.csv "/user/w205/hospital_compare/effective_care"
hdfs dfs -put $TMP_DIR/readmissions.csv "/user/w205/hospital_compare/readmissions"
hdfs dfs -put $TMP_DIR/measures.csv "/user/w205/hospital_compare/measures"
hdfs dfs -put $TMP_DIR/survey_responses.csv "/user/w205/hospital_compare/survey_responses"

# Remove temporary data directory used for extracting the raw data files
rm -r $TMP_DIR

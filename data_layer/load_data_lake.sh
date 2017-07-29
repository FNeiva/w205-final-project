#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Data Layer: Data Lake Loading script
#
# This is the first script in the pipeline, and in the data layer. It will pull the
# original data from the source(s) and upload it to our data lake, as-is, without any
# transformation. Data will be transformed later and stored in another location,
# preserving the original data.
##########################################################################################

echo "################################################"
echo "Dengue Fever Prediction System"
echo "Data Layer: Data Lake Loading Script"
echo "################################################"
echo " "
echo "Loading Data Lake:"

# Set temporary directory for extracting raw data files from the zip file
TMP_DIR=/data/tmp_data

# Remove old temporary directory if exists and then recreate
echo "		Creating temporary directory..."
if [ -d $TMP_DIR ] ; then
	rm -r $TMP_DIR
fi
mkdir $TMP_DIR
echo "		Temporary directory created!"


# Download files to the temporary directory
echo "		Downloading data files to temporary directory..."
wget -O $TMP_DIR/dengai_train_feature_data.csv "https://s3.amazonaws.com/drivendata/data/44/public/dengue_features_train.csv"
wget -O $TMP_DIR/dengai_train_labels_data.csv "https://s3.amazonaws.com/drivendata/data/44/public/dengue_labels_train.csv"
wget -O $TMP_DIR/dengai_test_feature_data.csv "https://s3.amazonaws.com/drivendata/data/44/public/dengue_features_test.csv"
echo "		Data downloaded successfully!"

# Strip the first line and rename the files we are interested in
echo "		Stripping data headers..."
tail -n +2 $TMP_DIR/"dengai_train_feature_data.csv" > $TMP_DIR/dengai_train_feature_noheader.csv
tail -n +2 $TMP_DIR/"dengai_train_labels_data.csv" > $TMP_DIR/dengai_train_labels_noheader.csv
tail -n +2 $TMP_DIR/"dengai_test_feature_data.csv" > $TMP_DIR/dengai_test_feature_noheader.csv
echo "		Data headers stripped!"

# Clean existing directories and files in HDFS to remove possible old files
echo "		Clear existing data lake directory..."
hdfs dfs -rm -r "/user/w205/dengue_prediction/original_data"
echo "		Data lake directory cleared!"

# Recreate directory structure in the HDFS data lake
echo "		Creating data lake directory structure..."
hdfs dfs -mkdir "/user/w205/dengue_prediction"
hdfs dfs -mkdir "/user/w205/dengue_prediction/original_data"
echo "		Directory structure created!"

# Load files into the HDFS data lake directory structure
echo "		Loading files into the data lake..."
hdfs dfs -put $TMP_DIR/dengai_train_feature_noheader.csv "/user/w205/dengue_prediction/original_data"
hdfs dfs -put $TMP_DIR/dengai_train_labels_noheader.csv "/user/w205/dengue_prediction/original_data"
hdfs dfs -put $TMP_DIR/dengai_test_feature_noheader.csv "/user/w205/dengue_prediction/original_data"
echo "		Data files loaded into the data lake!"

# Remove temporary data directory used for extracting the raw data files
echo "		Removing temporary directory..."
rm -r $TMP_DIR
echo "		Temporary directory removed!"

# All done
echo "Data lake loading finished successfully!"

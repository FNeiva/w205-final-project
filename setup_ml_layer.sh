#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Machine Learning Layer Initialization Script
#
# This is the super script that runs the entire Machine Learning Layer pipeline. It will:
#
#     * Delete the existing persisted model in HDFS
#     * Read the transformed data from HDFS
#     * Train the new model using the transformed data
#     * Persist the newly trained model to HDFS
#
# Be aware that this script may take a long time to run in order to fit the model.
#
##########################################################################################

# The following export fixes problems with PySpark not finding the native Hadoop library
LD_LIBRARY_PATH=/opt/jdk1.7.0_79/jre/lib/amd64/server/:/usr/lib/hadoop/lib/native/
export LD_LIBRARY_PATH

echo "##########################################################"
echo "Dengue Fever Prediction System"
echo "Machine Learning Layer Initialization and Update Script"
echo "##########################################################"
echo " "
echo "This script will now initialize or update the Machine Learning Layer."
echo "It will run other scripts to remove the old model, train and persist the new model."
echo "Be aware that fitting the new model may take a long time, so please wait until it is finished."
echo " "
echo " "
echo "Step 1 of 2: Deleting current persisted model... "
echo " "
echo " "
./ml_layer/delete_model.sh
echo " "
echo "Step 1 of 3 done."
echo " "
echo "Step 2 of 2: Training and persisting new model... "
echo " "
echo " "
/data/spark15/bin/spark-submit ./ml_layer/train_ml_model.py
echo " "
echo "Step 2 of 2 done."
echo " "
echo "Machine Learning Initialization and Update Script Finished!"

#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Machine Learning Layer: Model Training script
#
# This is the fourth script in the pipeline, and first in the ML layer. This script will
# delete any existing ML model persisted to HDFS to avoid errors when training a new
# ML model and persisting it to HDFS.
#
##########################################################################################

echo "################################################"
echo "Dengue Fever Prediction System"
echo "Machine Learning Layer: Model Deletion Script"
echo "################################################"
echo " "
echo "Deleting existing ML model..."

# Deletes the current model from HDFS
hdfs dfs -rm -r /user/w205/dengue_prediction/ml_model

echo "Current ML model deleted!"

#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Streaming Layer Initialization Script
#
# This is the super script that sets up the streaming layer. It will:
#
#     * Create the required PostgreSQL database
#     * Set up the Dark Sky Weather API Key as an environment variable
#
# Dark Sky Weather API Key may be freely obtainable at:
#     https://darksky.net/dev
#
##########################################################################################

# The following export fixes problems with PySpark not finding the native Hadoop library
LD_LIBRARY_PATH=/opt/jdk1.7.0_79/jre/lib/amd64/server/:/usr/lib/hadoop/lib/native/
export LD_LIBRARY_PATH

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "##########################################################"
echo "Dengue Fever Prediction System"
echo "Streaming Layer Initialization and Update Script"
echo "##########################################################"
echo " "
echo "This script will now initialize the Streaming Layer."
echo "It will run other scripts to create the PostgreSQL database, set up API Key and the streaming update rate."
echo " "
echo " "
echo "Step 1 of 2: Executing database creation script... "
echo " "
echo " "
python2.7 $DIR/streaming_layer/create_postgres_db.py
echo " "
echo "Step 1 of 2 done."
echo " "
echo "Step 2 of 2: Setting up Dark Sky Weather streaming... "
echo " "
echo "Please insert your Dark Sky Weather API Key and press [ENTER]"
read ds_key
echo " "
echo "Please insert the desired weather streaming update rate (in seconds) and press [ENTER]"
echo "Be aware that one API call is made per tracked city at every update. (default: 600)"
read update_rate

if [ -z ${update_rate} ]; then
      update_rate=600
fi

echo " "
echo -n "Do you want to persist configuration to your user profile? [y/N] "
read persist

if [ -z ${persist} ]; then
      persist="N"
fi

if [ "$persist" == 'y' ] || [ "$persist" == 'Y' ] || [ "$persist" == 'Yes' ] || [ "$persist" == 'yes' ] || [ "$persist" == 'YES' ];  then
      echo "export DARK_SKY_API_KEY="$ds_key >> ~/.bashrc
      echo "export DENGUE_PRED_STREAM_UPD_RATE="$update_rate >> ~/.bashrc
fi

echo "Exporting environment variables..."
export DARK_SKY_API_KEY=$ds_key
export DENGUE_PRED_STREAM_UPD_RATE=$update_rate
echo " "
echo "Step 2 of 2 done."
echo " "
echo "Streaming Layer Initialization and Update Script Finished!"

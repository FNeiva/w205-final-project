#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Visualization Layer Initialization Script
#
# This is the super script that sets up the visualization layer. It will:
#
#     * Set up the Mapbox Access Token as an environment variable
#
# Mapbox Access Token may be freely obtainable by signing up for the Starter plan at:
#     https://www.mapbox.com/
#
##########################################################################################

# The following export fixes problems with PySpark not finding the native Hadoop library
LD_LIBRARY_PATH=/opt/jdk1.7.0_79/jre/lib/amd64/server/:/usr/lib/hadoop/lib/native/
export LD_LIBRARY_PATH

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "##########################################################"
echo "Dengue Fever Prediction System"
echo "Visualization Layer Initialization Script"
echo "##########################################################"
echo " "
echo "This script will configure the Visualization Layer."
echo "It will set up the Mapbox Access Token used to gather map data."
echo " "
echo " "
echo "Step 1 of 1: Setting up Mapbox map interface... "
echo " "
echo "Please insert your Mapbox Access Token and press [ENTER]"
read mapbox_at
echo " "
echo -n "Do you want to persist configuration to your user profile? [y/N] "
read persist

if [ -z ${persist} ]; then
      persist="N"
fi

if [ "$persist" == 'y' ] || [ "$persist" == 'Y' ] || [ "$persist" == 'Yes' ] || [ "$persist" == 'yes' ] || [ "$persist" == 'YES' ];  then
      echo "export MAPBOX_ACCESS_TOKEN="$mapbox_at >> ~/.bashrc
fi

echo "Exporting environment variables..."
export MAPBOX_ACCESS_TOKEN=$mapbox_at
echo " "
echo "Step 1 of 1 done."
echo " "
echo "Visualization Layer Initialization Script Finished!"

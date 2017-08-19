#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Application start-up script
#
# This script starts the application by running the weather prediction streaming
# layer and starting up the visualization layer.
#
##########################################################################################

# The following export fixes problems with PySpark not finding the native Hadoop library
LD_LIBRARY_PATH=/opt/jdk1.7.0_79/jre/lib/amd64/server/:/usr/lib/hadoop/lib/native/
export LD_LIBRARY_PATH

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "##########################################################"
echo "Dengue Fever Prediction System"
echo "Start-up Script"
echo "##########################################################"
echo " "
echo "Starting up the Dengue Prediction System..."
echo " "

if [ -z ${DARK_SKY_API_KEY} ]; then
      echo "ERROR: Dark Sky Weather API Key not found!"
      echo "Please run '. ./setup_streaming_layer.sh' to configure the application"
      exit 1
fi

echo "  * Booting up Weather Streaming service..."
nohup /data/spark15/bin/spark-submit $DIR/streaming_layer/weather_updater.py > $DIR/logs/streaming.log 2> /dev/null &
pid=$!
echo "  * Weather Streaming service running! PID: "$pid
echo $pid >> $DIR/streaming.pid

echo "  * Booting up Dashboard service..."
nohup python2.7 $DIR/visualization_layer/dashboard.py > $DIR/logs/visualization.log 2> /dev/null &
pid=$!
echo "  * Dashboard service running! PID: "$pid
echo $pid >> $DIR/visualization.pid

echo " "
echo "Dengue Prediction System started!"
echo " "
hostname=`hostname`
echo "Dashboard available at http://$hostname:8050"
echo "To stop the application, run stop_application.sh"

#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Application shutdown script
#
# This script shuts down the application by killing the running streaming and
# visualization layers.
#
##########################################################################################

# The following export fixes problems with PySpark not finding the native Hadoop library
LD_LIBRARY_PATH=/opt/jdk1.7.0_79/jre/lib/amd64/server/:/usr/lib/hadoop/lib/native/
export LD_LIBRARY_PATH

# Get script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "##########################################################"
echo "Dengue Fever Prediction System"
echo "Shutdown Script"
echo "##########################################################"
echo " "
echo "Bringing down the Dengue Prediction System..."
echo " "
echo "  * Killing the Weather Streaming service..."

if [ ! -f $DIR/streaming.pid ]; then
      echo "ERROR: Streaming service PID not found! Please check if it is indeed running."
      exit 1
fi

pid=`cat $DIR/streaming.pid`
pkill -SIGTERM -g $(ps -o pgid -p $pid | grep -o [0-9]*)
rm -f $DIR/streaming.pid

echo "  * Weather Streaming service killed!"
echo "  * Killing the Dashboard service..."

if [ ! -f $DIR/visualization.pid ]; then
      echo "ERROR: Visualization service PID not found! Please check if it is indeed running."
      exit 1
fi

pid=`cat $DIR/visualization.pid`
pkill -SIGTERM -g $(ps -o pgid -p $pid | grep -o [0-9]*)
rm -f $DIR/visualization.pid

echo "  * Dashboard service killed!"
echo " "
echo "Dengue Prediction System stopped."

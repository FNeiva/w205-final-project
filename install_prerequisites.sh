#!/bin/bash

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Pre-requisite Installation Script
#
# This script installs Python packages and software that are required to run this
# project. Please note that it will NOT install PostgreSQL, Spark and Hadoop, which
# are provided in the UCB AMI that should be used for this project.
#
# THIS SCRIPT MUST BE EXECUTED AS THE ROOT USER
#
##########################################################################################

echo "################################################"
echo "Dengue Fever Prediction System"
echo "Pre-requisite Installation Script"
echo "################################################"
echo " "
echo "This script will now install all pre-requisites for running the project."
echo "Please wait."
echo " "
echo " "
echo "Installing Dash packages for Python 2.7... "
# Need to install and use Python 2.7
# AMI needs easy_install-2.7 and pip-2.7 for this
wget https://bootstrap.pypa.io/ez_setup.py -O - | python2.7        # Install easy_install-2.7
easy_install-2.7 pip                                               # Install pip2.7
# Set back easy_install-2.6 and pip2.6 as defaults to avoid other stuff from breaking
ln -sf /usr/bin/pip2.6 /usr/bin/pip
ln -sf /usr/bin/pip2.6 /usr/bin/pip2
ln -sf /usr/bin/easy_install-2.6 /usr/bin/easy_install
# Now install Dash on Python 2.7
pip2.7 install dash==0.17.7                                        # The core dash backend
pip2.7 install dash-renderer==0.7.4                                # The dash front-end
pip2.7 install dash-html-components==0.7.0                         # HTML components
pip2.7 install dash-core-components==0.12.0                        # Supercharged components
echo "Dash installed!"
echo " "
echo "Installing Plotly package for Python 2.7... "
pip2.7 install plotly==2.0.13                                      # Plotly graphing library used in examples
echo "Plotly installed!"
echo " "
echo "Installing Numpy package for Python 2.7... "
pip2.7 install numpy                                               # Install Numpy to use in PySpark
echo "Numpy installed!"
echo " "
echo "Installing Pandas package for Python 2.7... "
pip2.7 install pandas                                              # Install Pandas to use in PySpark
echo "Pandas installed!"
echo " "
echo "Installing PsycoPG2 package for Python 2.7... "
pip2.7 install psycopg2                                            # Install PsycoPG2 to use PostgreSQL
echo "PsycoPG2 installed!"
echo " "
echo "Installing Dark Sky API Wrapper package for Python 2.7... "
pip2.7 install python-forecastio                                   # Weather API for Dark Sky
echo "Dark Sky API Wrapper installed!"
echo " "
echo "Pre-requisite installation finished!"

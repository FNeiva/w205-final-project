# Dengue Prediction System
## MIDS W205 Final Project - Summer 2017

This application provides a full machine learning pipeline to analyze and predict the number of dengue cases for the next seven days through the use of live weather data. It currently supports prediction in six cities: San Juan, Iquitos, Sao Paulo, Brasilia, Rio de Janeiro and Salvador. In the future, this system may be expanded to other cities around the world.

The system currently employs [Dark Sky](https://darksky.net "Dark Sky") for frequent weather forecast updates used for Dengue predictions and [Mapbox](https://www.mapbox.com "Mapbox") for the maps used in visualization.

## Quick-start Guide On How To Run The Application

This quick-start section will guide you towards getting the application running in a short time. For more detailed information, please look at the Architecture document in the "docs" folder.

### Pre-requisites

This application was built and designed to run using the **UCB W205 Spring 2016 (ami-be0d5fd4)** AMI on AWS. In addition to all the software pre-installed in the AMI, you will also need the following:

**On Python 2.7:**
- python27-devel system package (installed using Yum)
- cyrus-sasl-devel system package (installed using Yum)
- Dash Python package (version 0.17.7, installed using pip2.7)
- Dash-renderer Python package (version 0.7.4, installed using pip2.7)
- Dash-html-components Python package (version 0.7.0, installed using pip2.7)
- Dash-core-components Python package (version 0.12.0, installed using pip2.7)
- Plotly Python package (version 2.0.13, installed using pip2.7)
- Numpy Python package (installed using pip2.7)
- Pandas Python package (installed using pip2.7)
- Psycopg2 Python package (installed using pip2.7)
- sasl Python package (installed using pip2.7)
- Thrift Python package (installed using pip2.7)
- Thrift-sasl Python package (installed using pip2.7)
- PyHive Python package (installed using pip2.7)
- Forecastio Python package (installed using pip2.7)

**On Python 2.6:**
- Numpy Python package (installed using pip)
- Pandas Python package (installed using pip)
- Psycopg2 Python package (installed using pip)
- Forecastio Python package (installed using pip)

**API Keys and Access Tokens:**
- Dark Sky Weather API Key (freely obtained at [https://darksky.net/dev/](https://darksky.net/dev/ "Dark Sky"))
- Mapbox Access Token (freely obtained by registering for a Starter account at [https://www.mapbox.com](https://www.mapbox.com "Mapbox"))

You can easily install all required system and Python packages using the provided *install_prerequisites.sh* script. The script performs all operations required on a configured AMI to get all requirements ready. As the **root** user, just run the following command from the project root directory:

~~~~
./install_prerequisites.sh
~~~~

You can also perform the installation of the packages manually by running, as the **root** user:

~~~~
yum -y install python27-devel cyrus-sasl-devel
wget https://bootstrap.pypa.io/ez_setup.py -O - | python2.7
easy_install-2.7 pip
ln -sf /usr/bin/pip2.6 /usr/bin/pip
ln -sf /usr/bin/pip2.6 /usr/bin/pip2
ln -sf /usr/bin/easy_install-2.6 /usr/bin/easy_install
pip2.7 install dash==0.17.7                                        
pip2.7 install dash-renderer==0.7.4                               
pip2.7 install dash-html-components==0.7.0                         
pip2.7 install dash-core-components==0.12.0
pip2.7 install plotly==2.0.13
pip2.7 install numpy
pip2.7 install pandas
pip2.7 install psycopg2                        
pip2.7 install sasl
pip2.7 install Thrift
pip2.7 install Thrift-sasl
pip2.7 install PyHive
pip2.7 install python-forecastio
pip install psycopg2
pip install python-forecastio
~~~~

After getting all pre-requisites installed, you may proceed to configuring the appplication.

### Before running the application

Before running or configuring the application, make sure you have the following started and working on your AMI:

- Started PostgreSQL (as **root**, run */data/start_postgres.sh*)
- Started Hadoop (as **root**, run */root/start-hadoop.sh*)
- Started the Hive Metastore (as **w205**, run */data/start_metastore.sh*)
- Started Hive Server (as **w205**, run *hive --service hiveserver2 &*)

To be able to access the visualization interface through a web browser, you will also need to open port **8050** on your EC2 instance through the AWS console.

### Application Configuration

To gather weather forecast updates, this application leverages the power of Dark Sky. Therefore, you will need a Dark Sky API Key that is freely obtainable at [https://darksky.net/dev](https://darksky.net/dev "Dark Sky API Key"). Please note that Dark Sky free API keys only allow for 1,000 API calls per day and charges for additional calls. This application makes one API call per monitored city at each data update, so keep that in mind when configuring the update interval. At the current level of six monitored cities, an update interval of two minutes (120 seconds) is enough to keep the application inside the free usage tier.

To be able to display maps in the visualization interface, this software also uses Mapbox, for which you will also need an Access Token. Mapbox Access Tokens are also freely obtained by registering for a Starter account at [https://www.mapbox.com](https://www.mapbox.com "Mapbox"). Mapbox gives you the option of using a provided public access token or generating new, private tokens. For this application, a private token is not necessary and you can simply use the provided public access token.

Configuring the application consists of:
- Downloading all required data and loading it into HDFS (Data Layer)
- Transforming all the data for analysis and Machine learning (Data Layer)
- Creating a Hive/SparkSQL schema for analysis of historical data (Data Layer)
- Training a machine learning algorithm on the historical data (Machine Learning Layer)
- Setting up a PostgreSQL database for storage and update of live predictions (Streaming Layer)
- Configuring Dark Sky API Keys (Streaming Layer)
- Configuring Mapbox Access Token (Visualization Layer)

Scripts for automatic configuration and setup of each layer are provided individually. This is so you have freedom to update and re-configure layers individually without affecting other layers. The configuration of each layer is described in detail below. Please note that, for the first time configuration, **you must configure components in the order described below** as they are inter-dependent. Any other subsequent re-configuration or update can be performed individually on each layer as required.

#### Data Layer Setup and Initialization ####

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_data_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the configuration script **using the following syntax**:

~~~~
. ./setup_data_layer.sh
~~~~

4. The script will download all required data to the instance's hard drive first, which may take some time. Please be patient as some of the files are big. It will then make small transformations on them and place them into HDFS, inside directory "/user/w205/dengue_prediction/original_data", then run the bigger transformations using Spark and save the transformed data into HDFS, inside directory "/user/w205/dengue_prediction/transformed_data".

5. If you run any posterior update to the data, you will need to stop and start the application in order for the new data to appear in the visualization layer. You will also need to re-run the Machine Learning configuration script to re-train the Machine Learning model using the new data.

#### Machine Learning Layer Setup and Initialization ####

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_ml_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the configuration script **using the following syntax**:

~~~~
. ./setup_ml_layer.sh
~~~~

4. The script will gather the previously transformed data, train a machine learning model using it and then persist the trained model to HDFS. Please be patient as training the model may take some time.

5. If you need to re-train the machine learning model in the future to use new data in the data layer, you can just re-run this script. Please note that you do not need to stop the application to re-train the model. You can keep it running while the model is re-trained, and when the script is finished just stop and start the application to load the newly trained model. This is designed to keep downtime as small as possible on eventual updates, given that re-training the model may take great amount of time.

#### Machine Learning Layer Setup and Initialization ####

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_ml_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the configuration script **using the following syntax**:

~~~~
. ./setup_ml_layer.sh
~~~~

4. The script will gather the previously transformed data, train a machine learning model using it and then persist the trained model to HDFS. Please be patient as training the model may take some time.

5. If you need to re-train the machine learning model in the future to use new data in the data layer, you can just re-run this script. Please note that you do not need to stop the application to re-train the model. You can keep it running while the model is re-trained, and when the script is finished just stop and start the application to load the newly trained model. This is designed to keep downtime as small as possible on eventual updates, given that re-training the model may take great amount of time.

#### Streaming Layer Setup and Initialization ####

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_streaming_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the configuration script **using the following syntax**:

~~~~
. ./setup_streaming_layer.sh
~~~~

4. This script will create the PostgreSQL database and tables in the local PostgreSQL Server (if they don't already exist).

5. Next, it will ask you for your Dark Sky API Key. Insert the key you obtained from Dark Sky and press <enter>.

6. The script will then ask you if you want to persist the configuration. Persisting it adds the Dark Sky key to your user profile script, so that in every new session it is reloaded automatically and you won't need to reconfigure the Streaming Layer before running the application after logging out of the current session. Type 'y' and press <enter> if you want to persist the key.

#### Visualization Layer Setup and Initialization ####

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_visualization_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the configuration script **using the following syntax**:

~~~~
. ./setup_visualization_layer.sh
~~~~

4. The script will ask you for your Mapbox Access Token. Insert the access token you obtained from Mapbox and press <enter>.

6. The script will then ask you if you want to persist the configuration. Persisting it adds the Mapbox Access Token to your user profile script, so that in every new session it is reloaded automatically and you won't need to reconfigure the Streaming Layer before running the application after logging out of the current session. Type 'y' and press <enter> if you want to persist the key.

#### Starting the application ####

To start the application, follow these steps:

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_visualization_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the start-up script:

~~~~
. ./start_application.sh
~~~~

4. **Please note:** after you start the application, a few seconds later some output from Spark may appear on screen. It is just Hive gathering the historical data to create the plots in the visualization layer. Just wait until an "OK" message is displayed on screen and it will be ready. This will only happen once, as the visualization layer caches historical data when it starts.

5. After the application is started, it will collect application logs into the "logs" folder.

6. To access the visualization interface, access the URL given by the start-up script in your browser. Please allow a few seconds for the service to boot-up, as it needs to cache the historical dengue data.

#### Stopping the application ####

**Please note:** you do not need to stop the application to perform data updates on the data layer or re-train the machine learning model. Run the configuration scripts for the data layer and machine learning layer while the application is still running, and just stop and start it after they are done. This is designed to reduce the amount of application downtime, as loading the data as re-training the machine learning model may take some time.

To stop the application, follow these steps.

1. If you are currently the *root* user, change to the *w205* user:

~~~~
su - w205
~~~~

2. Change to the project root directory, where the *setup_visualization_layer.sh* script is located. For instance, if you stored the project directory at */data/w205-final-project*, run:

~~~~
cd /data/w205-final-project
~~~~

3. Run the shutdown script:

~~~~
. ./stop_application.sh
~~~~

4. The application should be stopped.

#### Troubleshooting ####

The steps above have been tested many times, by different people and always using the specified AWS AMI. However, we understand that no matter the amount of testing problems may still occur. If that is the case, please get in touch with the authors or open an issue in our project GitHub webpage at [https://github.com/FNeiva/w205-final-project/issues](https://github.com/FNeiva/w205-final-project/issues "Project Issues Page").

**"Error gathering weather data for <city>!" error appearing in streaming.log**

Those errors can be caused by either a faulty Dark Sky API Key or by weather data unavailable for the city in the Dark Sky service. Check the error by accessing the Dark Sky website and trying their sample API call using the web browser. If you receive a 403 error, it could be because you reached the maximum daily amount of free API calls allowed. If it works, your API Key may have been renewed and changed. If that's the case, re-run the setup script for the Visualization layer and insert the new credentials, then stop and start the application.

##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Streaming Layer: Weather Updater script
#
# This is the main script in the streaming layer of the pipeline. This script tends to
# the "streaming" part, by constantly polling the Dark Sky Weather API for the next
# seven days weather prediction, runs the prediction on Spark MLLib using the stored
# model trained in the Machine Learning layer and stores results in the PostreSQL
# database for real-time analysis.
#
##########################################################################################

import numpy as np
import sys
import pyspark
import pyspark.sql.functions as psf
import forecastio
import psycopg2
import time
import os
from datetime import datetime
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import GradientBoostedTrees
from pyspark.mllib.tree import GradientBoostedTreesModel
from pyspark.mllib.linalg import SparseVector
from pyspark.mllib.evaluation import RegressionMetrics

print("################################################")
print("Dengue Fever Prediction System")
print("Streaming Layer: Weather Updater Daemon Script")
print("################################################")
print(" ")
print(str(datetime.now())+": Starting weather updater script")
print(str(datetime.now())+": Initiating SparkContext...")

# Initiate Spark Context
try:
    sc = SparkContext("local","dengue")
    sqlContext = SQLContext(sc)
except:
    print(str(datetime.now())+": Failed to initiate Spark Context!")
    print(str(datetime.now())+": Quitting...")
    sys.exit()

print(str(datetime.now())+": Loading trained ML model from HDFS...")

# Load trained model from HDFS
try:
    ml_model = GradientBoostedTreesModel.load(sc,"hdfs:///user/w205/dengue_prediction/ml_model")
except:
    print(str(datetime.now())+": Unable to load trained model from HDFS!")
    print(str(datetime.now())+": Quitting...")
    sys.exit()

print(str(datetime.now())+": Testing database connection...")

try:
    # Connect to the database
    conn = psycopg2.connect(database="denguepred", user="postgres", password="pass", host="localhost", port="5432")
    # Create cursor
    cur = conn.cursor()
    # Execute a query just to check that we don't get an exception
    cur.execute("SELECT * from predictions LIMIT 1;")
    # Try to fetch the result
    res = cur.fetchone()
    cur.close()
    conn.close()
except:
    print(str(datetime.now())+": Unable to connect to PostgreSQL database!")
    print(str(datetime.now())+": Quitting...")
    sys.exit()

print(str(datetime.now())+": Setting Dark Sky Weather API Key...")

if "DARK_SKY_API_KEY" in os.environ:
    ds_api_key = os.environ['DARK_SKY_API_KEY']
else:
    print(str(datetime.now())+": Dark Sky API Key Environment variable not found!")
    print(str(datetime.now())+": Quitting...")
    sys.exit()

print(str(datetime.now())+": All done. Starting real-time predictions...")

# Set cities to be read and their latitudes and longitudes
cities = {"San Juan":{"lat":18.4374,"long":-66.0045,"data":[1,0,0,0,0]},
          "Iquitos":{"lat":-3.7847,"long":-73.3086,"data":[0,1,0,0,0]},
          "Rio de Janeiro":{"lat":-22.9111,"long":-43.1649,"data":[0,0,1,0,0]},
          "Brasilia":{"lat":-15.8697,"long":-47.9172,"data":[0,0,0,1,0]},
          "Sao Paulo":{"lat":-23.6273,"long":-46.6566,"data":[0,0,0,0,1]},
          "Salvador":{"lat":-12.9111,"long":-38.3312,"data":[0,0,0,0,0]} }

# We will keep a simple prediction counter just to let out some updates every now and then
# Just so we know we are still alive
n_preds = 0
time_preds = 0
# Keep loop until we receive termination signal
while True:

    # Sets the update delay for 120 seconds
    # That is so we can be safely inside Dark Weather API's free daily usage
    upd_delay = 120
    time_start_pred = time.time()
    data = []
    # We need a separate list of cities from which we successfully gathered the weather forecast
    cities_pred = []
    # Iterate through every city, gather the prediction for next week
    for city in cities:
        info = cities[city]
        try:
            # Gather weather prediction for next seven days
            forecast = forecastio.load_forecast(ds_api_key, info["lat"], info["long"], units="si")
            daily = forecast.daily()
            # Get the data for the next seven days
            daily_data = daily.data
            # Remove the data point for current day
            daily_data = daily_data[1:]
            # Now get the values we need for each day
            max_temps = [x.temperatureMax for x in daily_data]
            min_temps = [x.temperatureMin for x in daily_data]
            dew_point_temps = [x.dewPoint for x in daily_data]
            rel_humidities = [x.humidity for x in daily_data]
            # Insert into array in the correct format
            city_data = info["data"]
            # Average temperature in Kelvin (Celsius + 273.15)
            city_data.append(np.mean(max_temps+min_temps)+273.15)
            # Dew Point temperature in Kelvin
            city_data.append(np.mean(dew_point_temps)+273.15)
            # Max temperature in K
            city_data.append(np.max(max_temps)+273.15)
            # Min temperature in K
            city_data.append(np.min(min_temps)+273.15)
            # Relative humidity in %
            city_data.append(np.mean(rel_humidities)*100.)
            # Average temperature in C
            city_data.append(np.mean(max_temps+min_temps))
            # Append city data to data array
            data.append(city_data)
            # We have successfully gathered the forecast for this city
            cities_pred.append(city)
        except:
            print(str(datetime.now())+": Error gathering weather data for %s!" % city)

    # Parallelize array
    rdd = sc.parallelize(data)
    # Run prediction
    preds = ml_model.predict(rdd).collect()
    wkfrstday = datetime.now().strftime("%Y-%m-%d")
    # Update PostgreSQL table into week starting today, using UPSERT style query
    # Therefore, if there is a row for the current year and week start date, update it
    # If not, insert a new one
    #try:
    conn = psycopg2.connect(database="denguepred", user="postgres", password="pass", host="localhost", port="5432")
    cur = conn.cursor()
    for i in range(len(cities_pred)):
        cur.execute("UPDATE predictions SET (avg_temp_K, dew_pt_temp_K, max_temp_K, min_temp_K, \
                                                rel_hum_pct, avg_temp_C, num_cases) = (%s,%s,%s,%s,%s,%s,%s)  \
                                                WHERE city=%s AND wkfrstday=%s;",
                                                (data[i][5],data[i][6],data[i][7],data[i][8],data[i][9],data[i][10],
                                                 preds[i],cities_pred[i],wkfrstday))
        cur.execute("INSERT INTO predictions (city,wkfrstday,avg_temp_K, dew_pt_temp_K, max_temp_K, min_temp_K, \
                                                  rel_hum_pct, avg_temp_C, num_cases) \
                        SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s WHERE NOT EXISTS \
                        (SELECT 1 FROM predictions WHERE city=%s AND wkfrstday=%s);",
                        (cities_pred[i],wkfrstday,data[i][5],data[i][6],data[i][7],data[i][8],data[i][9],data[i][10],
                         preds[i],cities_pred[i],wkfrstday))
        conn.commit()
        conn.close()
    #except:
    #    print(str(datetime.now())+": Unable to update database table with new predictions!")

    time_end_pred = time.time()
    n_preds += 1
    if (n_preds % 15 == 0):
        n_seconds = time_end_pred - time_start_pred
        time_preds += n_seconds
        print(str(datetime.now())+": Executed %d predictions so far. Average prediction time: %.3f seconds" % (n_preds,float(time_preds)/float(n_preds)))

    # All done, sleep during the update delay and come back later
    time.sleep(upd_delay)

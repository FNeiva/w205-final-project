##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Data Layer: Data Lake Transformation script
#
# This is the second script in the pipeline, and in the data layer. This script runs
# the PySpark script that transforms the original data in the data lake and stores it
# in HDFS for visualization of the historical data and training the Machine Learning
# model used for live predictions.
#
# As we are working with two different datasets, we need to put them into a common format
# and merge them into a single source. We currently have two datasets: one complete DengAI
# dataset from San Juan and Iquitos with full socioeconomic and weather data, summarized
# by number of cases per epidemiological week, and another from the Brazilian DATASUS.
# The Brazilian DATASUS database is regarded as one of the most complete Dengue datasets
# in the world. The file we have here includes every notification of Dengue case from
# XXXX to 2016, with the city they ocurred in and the date. We have pulled weather data,
# city data and weather station data to complement this dataset, so that it can be merged
# with the Iquitos and San Juan dataset. What this script does is:
#
#   * Summarize the Brazilian DATASUS data by city and epidemiological week
#   * Summarize weather data per epidemiological week for each region
#   * Merge summarized dengue cases data with summarized weather data
#   * Merge both DATASUS and DengAI datasets
#   * Rewrite the data as a single dataset to HDFS
#
##########################################################################################

import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import datetime
import numpy as np

print("################################################")
print("Dengue Fever Prediction System")
print("Data Layer: Data Lake Transformation Script")
print("################################################")
print(" ")
print("Transforming Data Lake:")
print("	* Loading original data sources...")

# Initiate Spark Context
sc = SparkContext("local", "dengue")
sqlContext = SQLContext(sc)

# Load all original data files
#dengai_data_features = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/dengai_train_feature_noheader.csv")
#dengai_data_targets = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/dengai_train_labels_noheader.csv")
dengai_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/dengai/dengai_data.csv")
datasus_notif_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/datasus_notifs/brazil_datasus_notifications_noheader.csv")
datasus_weather_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_weather_history/brazil_weather_history_noheader.csv")
datasus_station_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_weather_stations/brazil_weather_stations_noheader.csv")
datasus_city_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_cities/brazil_cities_noheader.csv")

print("	* Original data sources loaded!")
print("	* Transforming DengAI dataset...")

# Begin with DengAI, by dropping all non-weather features as we are not working with them at the moment
# These are the file columns:
# 0. City, 1. Year, 2. Week of Year, 3. Week start date, 4. Vegetation NE, 5. Veg. NW, 6. Veg. SE, 7. Veg. SW
# 8. Precipitation in mm, 9. Air temperature in K, 10. Avg. Temperature in K, 11. Dew Point Temp. in K,
# 12. Max. air temp. in K, 13. Min. air temp. in K, 14. Precipitation kg/m^2, 15. Relative humidity in %,
# 16. Sat. Precipitation in mm, 17. Specific Humidity in g/Kg, 18. Tdtr (?) in K, 19. Avg. Temperature in C,
# 20. Station diurnal temp. range in C, 21. Station Max. Temp. in C, 22. Station Min. Temperature in C,
# 23. Station precipitation in mm, 24. City (repeated), 25. Year (repeated), 26. Week of Year (repeated),
# 27. Number of cases

# Split the data on ',''
dengai_data = dengai_data.map(lambda x: x.split(','))
# Map values we want
dengai_data = dengai_data.map(lambda x: (x[0],x[1],x[2],x[10],x[11],x[12],x[13],x[15],x[19],x[27]))
# Build the schema and construct the Data Frame
schemaString = 'city year wkofyear avg_temp_K dew_pt_temp_K max_temp_K min_temp_K rel_hum_pct avg_temp_C num_cases'
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
dengai_df = sqlContext.createDataFrame(dengai_data, schema)
# Filter rows with null values
for col in dengai_df.columns:
    dengai_df = dengai_df.filter(df[col].isNotNull())
# Change column types
dengai_df = dengai_df.withColumn("avg_temp_K", dengai_df["avg_temp_K"].cast(DoubleType()))
dengai_df = dengai_df.withColumn("dew_pt_temp_K", dengai_df["dew_pt_temp_K"].cast(DoubleType()))
dengai_df = dengai_df.withColumn("max_temp_K", dengai_df["max_temp_K"].cast(DoubleType()))
dengai_df = dengai_df.withColumn("min_temp_K", dengai_df["min_temp_K"].cast(DoubleType()))
dengai_df = dengai_df.withColumn("rel_hum_pct", dengai_df["rel_hum_pct"].cast(DoubleType()))
dengai_df = dengai_df.withColumn("avg_temp_C", dengai_df["avg_temp_C"].cast(DoubleType()))
dengai_df = dengai_df.withColumn("num_cases", dengai_df["num_cases"].cast(IntegerType()))

print("	* DengAI dataset transformed!")
print("	* Transforming DATASUS dataset...")

# Set up a dictionary to map a weather station to a city geocode
# There certainly is a better way of doing this by using latitude and longitude, for instance,
# but we are doing this for ease of implementation for now
station2cities = {"SBRJ":"3304557",             # Rio de Janeiro
                  "SBBR":"5300108",             # Brasilia
                  "SBSP":"3550308",             # Sao Paulo
                  "SBSV":"2927408"}             # Salvador

datasus_weather_data = datasus_weather_data.map(lambda x: x.split(','))
datasus_weather_data = datasus_weather_data.filter(lambda x: x[0] in station2cities)
datasus_weather = datasus_weather_data.map(lambda x: (station2cities[x[0]],
                                                      datetime.strptime(x[3],"%Y-%m-%d").isocalendar()[0],      # Year
                                                      datetime.strptime(x[3],"%Y-%m-%d").isocalendar()[1],      # Week of Year
                                                      float(x[2])+273.15,
                                                      243.04*(np.log(float(x[5])/100)+((17.625*float(x[2]))/(243.04+float(x[2]))))/(17.625-np.log(float(x[5])/100)-((17.625*float(x[2]))/(243.04+float(x[2])))),
                                                      float(x[1]), float(x[0]), float(x[5]),float(x[2])))

datasus_notif_data = datasus_notif_data.map(lambda x: x.split(','))


print("	* DATASUS dataset transformed!")
print("	* Merging datasets...")

dengue_data = dengai_df

print("	* Datasets merged!")
print("	* Writing resulting dataset to HDFS...")

# Use the spark-csv extension to write the file as CSV since we are using Spark 1.5
dengue_data.write.format("com.databricks.spark.csv").save("hdfs:///user/w205/dengue_prediction/transformed_data/dengue_data.csv")

print("	* Dataset HDFS write finished!")
print("Data lake transformation finished successfully!")

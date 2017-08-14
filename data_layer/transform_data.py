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

print("################################################")
print("Dengue Fever Prediction System")
print("Data Layer: Data Lake Transformation Script")
print("################################################")
print(" ")
print("Transforming Data Lake:")
print("	* Loading original data sources...")

# Initiate Spark Context
sc = SparkContext("local", "dengue")

# Load all original data files
#dengai_data_features = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/dengai_train_feature_noheader.csv")
#dengai_data_targets = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/dengai_train_labels_noheader.csv")
dengai_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/dengai_data.csv")
datasus_notif_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_datasus_notifications_noheader.csv")
datasus_weather_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_weather_history_noheader.csv")
datasus_station_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_weather_stations_noheader.csv")
datasus_city_data = sc.textFile("hdfs:///user/w205/dengue_prediction/original_data/brazil_cities_noheader.csv")

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
dengai_data_features = dengai_data_features.map(lambda x: x.split(','))
dengai_data_features = dengai_data_features.map(lambda x: (x[0],x[1],x[2],x[9],x[10],x[11],x[12],x[13],x[15],x[17],x[19],x[21],x[22],x[27]))

print("	* DengAI dataset transformed!")
print("	* Transforming DATASUS dataset...")



print("	* DATASUS dataset transformed!")
print("	* Merging datasets...")



print("	* Datasets merged!")
print("	* Writing resulting dataset to HDFS...")

dengai_data.saveAsTextFile("file:///data/test.txt")

print("	* Dataset HDFS write finished!")
print("Data lake transformation finished successfully!")

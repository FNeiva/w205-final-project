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

from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql import SQLContext
import datetime

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
dengai_data = dengai_data.map(lambda x: x.split(','))
dengai_cases = dengai_data.map(lambda x: Row(city=x[0],year=x[1],wkofyear=int(x[2]),airtemp=int(x[9]),avgtemp=int(x[10]),
                                            dewpttemp=int(x[11]),maxtemp=int(x[12]),mintemp=int(x[13]),relhum=int(x[15]),
                                            sphum=int(x[17]),avgtempc=int(x[19]),stationmaxtemp=int(x[21]),
                                            stationmintemp=int(x[22]), numcases=int(x[27])))
dengai_df = sqlContext.createDataFrame(dengai_cases)

print("	* DengAI dataset transformed!")
print("	* Transforming DATASUS dataset...")

# DATASUS Notification data file columns are:
# 0. ID, 1. Date of notification, 2. Week of Year of notification, 3. Year of notification, 4. Date of first sign,
# 5. Week of Year of first sign, 6. Date of insertion, 7. Neighborhood, 8. Neighborhood ID, 9. City Geocode,
# 10. Notification number, 11. CID Code (mapping to disease manifestation)
datasus_notif_data = datasus_notif_data.map(lambda x: x.split(','))
datasus_notifs = datasus_notif_data.map(lambda x: Row(city=x[9],year=x[3],wkofyear=int(x[2])))
datasus_df = sqlContext.createDataFrame(datasus_notifs)
datasus_df = datasus_df.groupBy(['city','year','wkofyear']).count()
datasus_df['numcases'] = datasus_df['count']
datasus_df = datasus_df.drop('count') 

print("	* DATASUS dataset transformed!")
print("	* Merging datasets...")



print("	* Datasets merged!")
print("	* Writing resulting dataset to HDFS...")

print("	* Dataset HDFS write finished!")
print("Data lake transformation finished successfully!")

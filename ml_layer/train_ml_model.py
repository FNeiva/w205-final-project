##########################################################################################
# Dengue Fever Prediction System
# W205 Summer 2017 Final Project
# Felipe Campos, Frank Shannon, Josh Wilson and Matthew Holmes
##########################################################################################
# Machine Learning Layer: Model Training script
#
# This is the fifth script in the pipeline, and second in the ML layer. This script will
# run multiple tasks related to processing the dataset as required for ML, training and
# tuning the model and then storing the trained model for easy and quick retrieval by
# the streaming layer for predicting dengue cases on live data.
#
##########################################################################################

import pyspark
import pyspark.sql.functions as psf
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import GradientBoostedTrees
from pyspark.mllib.linalg import SparseVector
from pyspark.mllib.evaluation import RegressionMetrics

print("################################################")
print("Dengue Fever Prediction System")
print("Machine Learning Layer: Model Training Script")
print("################################################")
print(" ")
print("Performing Machine Learning model training:")

# Initiate Spark Context
sc = SparkContext("local", "dengue")
sqlContext = SQLContext(sc)

print("     * Reading transformed data... ")

# Load transformed data
training_data = sc.textFile("hdfs:///user/w205/dengue_prediction/transformed_data/dengue_data.csv")
# Split the data on ',''
training_data = training_data.map(lambda x: x.split(','))
# Map columns
training_data = training_data.map(lambda x: (x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]))
# Build the schema and construct the Data Frame
schemaString = 'city year wkofyear avg_temp_K dew_pt_temp_K max_temp_K min_temp_K rel_hum_pct avg_temp_C num_cases'
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
training_df = sqlContext.createDataFrame(training_data, schema)

print("     * Transformed data read!")
print("     * Reshaping the data for ML training... ")

# We need to make dummy variables for each city
cities = training_df.select("city").distinct().rdd.map(lambda r: r[0]).collect()
colnames = []
for city in cities:
    column_name = "city_"+city.replace(" ","_")
    training_df = training_df.withColumn(column_name, psf.when(training_df["city"] == city,1).otherwise(0))
    colnames.append(column_name)
# Drop one city from dummy variable to avoid multicollinearity
colnames = colnames[:-1]

# Change column types
training_df = training_df.withColumn("avg_temp_K", training_df["avg_temp_K"].cast(DoubleType()))
training_df = training_df.withColumn("dew_pt_temp_K", training_df["dew_pt_temp_K"].cast(DoubleType()))
training_df = training_df.withColumn("max_temp_K", training_df["max_temp_K"].cast(DoubleType()))
training_df = training_df.withColumn("min_temp_K", training_df["min_temp_K"].cast(DoubleType()))
training_df = training_df.withColumn("rel_hum_pct", training_df["rel_hum_pct"].cast(DoubleType()))
training_df = training_df.withColumn("avg_temp_C", training_df["avg_temp_C"].cast(DoubleType()))
training_df = training_df.withColumn("num_cases", training_df["num_cases"].cast(IntegerType()))

# Select columns to be used
colnames.append("avg_temp_K")
colnames.append("dew_pt_temp_K")
colnames.append("max_temp_K")
colnames.append("min_temp_K")
colnames.append("rel_hum_pct")
colnames.append("avg_temp_C")
colnames.append("num_cases")
training_df = training_df.select(colnames)

print("     * Data reshape finished!")
print("     * Training test ML model... ")

# Label the data points
labeled_data = training_df.map(lambda x: LabeledPoint(x[-1],x[:-1]))
# Separate training and testing data
training_data, testing_data = labeled_data.randomSplit([0.8, 0.2])
# Train the model
ml_model = GradientBoostedTrees.trainRegressor(training_data, {}, numIterations=10)

print("     * Model trained!")
print("     * Testing model error... ")

# Predict and calculate error metrics
predictions = ml_model.predict(testing_data.map(lambda r: r.features))
predictions.zip(testing_data.map(lambda r: r.label))
metrics = RegressionMetrics(predictions)

print("     * Model regression error metrics: ")
print("         - Mean Absolute Error: %.2f" % metrics.meanAbsoluteError)
print("         - Mean Squared Error: %.2f" % metrics.meanSquaredError)
print("         - Root Mean Squared Error: %.2f" % metrics.rootMeanSquaredError)
print("     * Training model with full data... ")

# Re-train model using full dataset
ml_model = GradientBoostedTrees.trainRegressor(labeled_data, {}, numIterations=10)

print("     * Persisting model to HDFS... ")

# Save the trained model
ml_model.save(sc,"hdfs:///user/w205/dengue_prediction/ml_model")

print("     * Trained model saved to HDFS")
print("Machine Learning Model training finished!")

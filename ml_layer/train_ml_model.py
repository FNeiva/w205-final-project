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
from pyspark.mllib.regression import LinearRegressionWithSGD
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

print("     * Reading transformed ML training data... ")

# Load transformed data
training_data = sc.textFile("hdfs:///user/w205/dengue_prediction/transformed_data/dengue_ml_training_set.csv")
# Split the data on ',''
training_data = training_data.map(lambda x: x.split(','))
# Map columns
training_data = training_data.map(lambda x: (int(x[0]),int(x[1]),int(x[2]),int(x[3]),float(x[4]),float(x[5]),float(x[6]),float(x[7]),float(x[8]),float(x[9]),int(x[10])))

# Build the schema and construct the Data Frame
schemaString = 'city0 city1 city2 city3 avg_temp_K dew_pt_temp_K max_temp_K min_temp_K rel_hum_pct avg_temp_C num_cases'
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
training_df = sqlContext.createDataFrame(training_data, schema).cache()

# Clear rows with missing values, for sanity checking
for col in training_df.columns:
    training_df = training_df.filter(training_df[col].isNotNull())

print("     * Transformed data read!")
#print("     * Reshaping the data for ML training... ")

# We need to make dummy variables for each city
#cities = training_df.select("city").distinct().rdd.map(lambda r: r[0]).collect()
#colnames = []
#for city in cities:
#    column_name = "city_"+city.replace(" ","_")
#    training_df = training_df.withColumn(column_name, psf.when(training_df["city"] == city,1).otherwise(0))
#    colnames.append(column_name)
# Drop one city from dummy variable to avoid multicollinearity
#colnames = colnames[:-1]

# Change column types
#training_df = training_df.withColumn("avg_temp_K", training_df["avg_temp_K"].cast(DoubleType()))
#training_df = training_df.withColumn("dew_pt_temp_K", training_df["dew_pt_temp_K"].cast(DoubleType()))
#training_df = training_df.withColumn("max_temp_K", training_df["max_temp_K"].cast(DoubleType()))
#training_df = training_df.withColumn("min_temp_K", training_df["min_temp_K"].cast(DoubleType()))
#training_df = training_df.withColumn("rel_hum_pct", training_df["rel_hum_pct"].cast(DoubleType()))
#training_df = training_df.withColumn("avg_temp_C", training_df["avg_temp_C"].cast(DoubleType()))
#training_df = training_df.withColumn("num_cases", training_df["num_cases"].cast(IntegerType()))



# Select columns to be used
#colnames.append("avg_temp_K")
#colnames.append("dew_pt_temp_K")
#colnames.append("max_temp_K")
#colnames.append("min_temp_K")
#colnames.append("rel_hum_pct")
#colnames.append("avg_temp_C")
#colnames.append("num_cases")
#training_df = training_df.select(colnames).cache()

#print("     * Data reshape finished!")
print("     * Training test ML model... ")

# Label the data points
labeled_data = training_df.map(lambda x: LabeledPoint(x[-1],x[:-1])).cache()
# Separate training and testing data
training_data, testing_data = labeled_data.randomSplit([0.8, 0.2])
# Train the model
ml_model = LinearRegressionWithSGD.train(training_data, iterations=100)

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
ml_model = LinearRegressionWithSGD.train(labeled_data, iterations=100)

print("     * Persisting model to HDFS... ")

# Save the trained model
ml_model.save(sc,"hdfs:///user/w205/dengue_prediction/ml_model")

print("     * Trained model saved to HDFS")
print("Machine Learning Model training finished!")

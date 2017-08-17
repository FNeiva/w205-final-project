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

import numpy as np
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
sc = SparkContext("local","dengue")
sqlContext = SQLContext(sc)

print("     * Reading transformed ML training data... ")

# Load transformed data
training_data = sc.textFile("hdfs:///user/w205/dengue_prediction/transformed_data/dengue_ml_training_set.csv")
# Split the data on ',''
training_data = training_data.map(lambda x: x.split(','))
# Map columns
training_data = training_data.map(lambda x: (int(x[0]),int(x[1]),int(x[2]),int(x[3]),
                                             int(x[4]),float(x[5]),float(x[6]),float(x[7]),
                                             float(x[8]),float(x[9]),float(x[10]),int(x[11])))
# Filter NaNs that may have made it into the dataset
training_data = training_data.filter(lambda x: ~np.isnan(x[0]) and ~np.isnan(x[1]) and ~np.isnan(x[2]) and ~np.isnan(x[3]) and
                                               ~np.isnan(x[4]) and ~np.isnan(x[5]) and ~np.isnan(x[6]) and ~np.isnan(x[7]) and
                                               ~np.isnan(x[8]) and ~np.isnan(x[9]) and ~np.isnan(x[10]) and ~np.isnan(x[11])).cache()

# We have to do something here to cache the dataset, otherwise it hangs later on due to a PySpark bug
num_records = training_data.count()

print("     * Transformed data read!")
print("     * Training test ML model... ")

# Label the data points
labeled_data = training_data.map(lambda x: LabeledPoint(x[-1],x[:-1]))
# Separate training and testing data
train_data, test_data = labeled_data.randomSplit([0.8, 0.2])
# Do something again to avoid the PySpark bug hang from manifesting
num_train_recs = train_data.count()
num_test_recs = test_data.count()
# Train the model
ml_model = GradientBoostedTrees.trainRegressor(train_data, {}, numIterations = 20, loss='leastAbsoluteError')

print("     * Model trained!")
print("     * Testing model error... ")

# Predict and calculate error metrics
predictions = ml_model.predict(test_data.map(lambda r: r.features))
predictions = predictions.zip(test_data.map(lambda r: r.label))
metrics = RegressionMetrics(predictions)

print("     * Model regression error metrics: ")
print("         - Mean Absolute Error: %.2f" % metrics.meanAbsoluteError)
print("         - Mean Squared Error: %.2f" % metrics.meanSquaredError)
print("         - Root Mean Squared Error: %.2f" % metrics.rootMeanSquaredError)
print("     * Training model with full data... ")

# Re-train model using full dataset
ml_model = GradientBoostedTrees.trainRegressor(labeled_data, {}, numIterations = 20, loss='leastAbsoluteError')

print("     * Persisting model to HDFS... ")

# Save the trained model
ml_model.save(sc,"hdfs:///user/w205/dengue_prediction/ml_model")

print("     * Trained model saved to HDFS")
print("Machine Learning Model training finished!")

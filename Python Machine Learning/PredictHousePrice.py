import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.datasets
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics
from sklearn.datasets import fetch_california_housing
import sys
import os

# Load the California housing dataset
california_housing = sklearn.datasets.fetch_california_housing()
print("California Housing Dataset:")
print(california_housing) 

# loading the dataset to a Pandas DataFrame
house_price_data =pd.DataFrame(california_housing.data,columns=california_housing.feature_names)

# print the first 5 rows of the dataset
print("First 5 rows of the dataset:")
print(house_price_data.head())

# loading the target variable
house_price_data['price'] = california_housing.target

# print the first 5 rows of the target variable
print("First 5 rows of dataset with price:")
print(house_price_data.head())

# checking the number of rows and cols
data_shape = house_price_data.shape

# checking for missing value
print(house_price_data.isnull().sum())

# getting the statics of the dataset
print("Statistics of the dataset:")
print(house_price_data.describe())

# correlation dataset
correlation = house_price_data.corr()

# constructing a heatmap to understand the correlation
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
#plt.show()

# splitting the data and target variable
X = house_price_data.drop('price', axis=1)
y = house_price_data['price']

print(X)
print(y)

# splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

print("X shape:", X.shape)
print("Training set shape:", X_train.shape)
print("Testing set shape:", X_test.shape)

# loading the XGBRegressor model
model = XGBRegressor()
# training the model
model.fit(X_train, y_train)

# making predictions on the training set
y_pred = model.predict(X_train)

# R squared error
r2_score = metrics.r2_score(y_train, y_pred)
print("R squared error:", r2_score)

# mean absolute error
mae = metrics.mean_absolute_error(y_train, y_pred)
print("Mean absolute error:", mae)

# making predictions on the testing set
y_test_pred = model.predict(X_test)

# R squared error
r2_score_test = metrics.r2_score(y_test, y_test_pred)
print("R squared error (test):", r2_score_test)

# mean absolute error
mae_test = metrics.mean_absolute_error(y_test, y_test_pred)
print("Mean absolute error (test):", mae_test)

# Visualizing the predictions
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_test_pred, color='blue', alpha=0.5)
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', linewidth=2)
plt.title('Actual vs Predicted Prices')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.grid()
plt.show()  
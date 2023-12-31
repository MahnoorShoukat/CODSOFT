# -*- coding: utf-8 -*-
"""MOVIE_RATING_PREDICTION.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_ucBI81BSVa0sdQJzkvq1xZhIEkddEzs

**Task 02 : MOVIE RATING PREDICTION WITH PYTHON**

Description: I have used the movie rating dataset to build a model that predicts the rating of a movie based on genre, director, and actors.

**FLOW ANALYSIS:**

* Importing Libraries

* Data loading

* Data Understanding

* Data Pre-Processing (Cleaning)

    *   Replacing missing values
    *   Extracting numerical values

* Spliting training and test data

* Model training -LinearRegression

* Model Evaluation - Prediction
"""

from google.colab import drive
drive.mount('/content/drive')

# Importing all the required libraries
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Dataset Loading
movie_review = pd.read_csv('/content/drive/MyDrive/CodSoft/IMDb Movies India.csv', encoding='latin-1')

"""**Data Understanding**"""

# Displaying the first 5 rows of the dataset
movie_review.head()

# Displaying total rows and columns of the dataset
movie_review.shape

# It will calculate and display count, mean, std, min, max, 25%, 50% and 75% of numeric columns here only "Rating" column.
movie_review.describe()

# Displaying information regarding datatype, null values of every column
movie_review.info()

# Checking for null values
movie_review.isna().sum()

"""**Data Cleaning**"""

movie_review['Duration'] = movie_review['Duration'].str.extract('(\d+)').astype(float)

# Fill missing values with the median value
median_duration = movie_review['Duration'].median()
movie_review['Duration'].fillna(median_duration, inplace=True)

movie_review['Votes'] = pd.to_numeric(movie_review['Votes'], errors='coerce')

# Fill missing values with the mean value
mean_votes = movie_review['Votes'].mean()
movie_review['Votes'].fillna(mean_votes, inplace=True)

# Handling missing values with mean for numerical columns and mode for categorical columns
movie_review['Genre'].fillna(movie_review['Genre'].mode()[0], inplace=True)
movie_review['Rating'].fillna(movie_review['Rating'].mean(), inplace=True)

movie_review['Actor 1'].fillna('Unknown', inplace=True)
movie_review['Actor 2'].fillna('Unknown', inplace=True)
movie_review['Actor 3'].fillna('Unknown', inplace=True)
movie_review['Director'].fillna('Unknown', inplace=True)

# Extract numeric year from the 'Year' column and convert to float
movie_review['Year'] = movie_review['Year'].str.extract('(\d+)').astype(float)

# Fill missing values with the median year or another appropriate strategy
median_year = movie_review['Year'].median()
movie_review['Year'].fillna(median_year, inplace=True)

movie_review.isnull().sum()

"""**One Hot Encoding**"""

movie_review = pd.get_dummies(movie_review, columns=['Genre'], prefix='Genre')

"""**Label Encoding**"""

label_encoders = {}
columns_to_label_encode = ['Director', 'Actor 1', 'Actor 2', 'Actor 3']

for column in columns_to_label_encode:
    label_encoder = LabelEncoder()
    movie_review[column] = label_encoder.fit_transform(movie_review[column])
    label_encoders[column] = label_encoder

# Splitting the training and testing dataset
X = movie_review[['Year', 'Duration'] + list(movie_review.filter(regex='Genre_').columns) + columns_to_label_encode]
y = movie_review['Rating']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = LinearRegression()
model.fit(X_train, y_train)

#Model Evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R-squared:", r2)
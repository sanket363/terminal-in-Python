# Consumption Forecast

### Introduction

This project aims to analyze and predict energy consumption using time-series data from Stuttgart and other house datasets. Through data cleaning, feature engineering, and advanced modeling techniques, we attempt to detect and correct anomalies, generate artificial features, and train an XGBoost model to produce accurate energy predictions. This project is particularly focused on handling complex time-series features and evaluating model performance on structured date splits.

### Objective

This project aims to build an energy consumption forecasting model that provides accurate predictions. By analyzing time-series data from Stuttgart and other sources, it focuses on capturing seasonal trends and daily patterns to offer reliable consumption forecasts for improved energy management and operational efficiency.

### Prerequisites

Python 3.8 or later
Pandas
NumPy
XGBoost
scikit-learn
matplotlib
holidays

### Installation

Clone this repository to your local machine.

git clone https://dev.azure.com/smartdings/new-move-energy/_git/newmove-consumption-forecast-assets

cd project-newmove-consumption-forecast-assets

Install dependencies.

pip install -r requirements.txt

### Approach

1. Data Fetching and Processing

- Fetch Weather Data: Retrieve weather data using the Visual Crossing API.
- Process Weather Data: Clean and filter the weather data, dropping unnecessary columns and ensuring correct date-time formats.
- Retrieve Energy Consumption Data: Fetch energy consumption data from the DynamoDB table new_hourly_data. Convert half-hourly data to hourly format.

2. Data Merging

- Merge Weather and Consumption Data: Combine the weather data and energy consumption data on a date-time basis to create a unified dataset.

3. Data Cleaning

- Outlier Detection and Smoothing: Identify and smooth outliers in the energy consumption column to ensure data quality.

4. Feature Engineering

- Add Artificial Features: Create additional features for date-time, temperature, and energy consumption columns to enhance model accuracy.
- Convert Home ID: Apply a hashing function to convert the Home ID column to an integer format, aiding in model processing.

5. Data Splitting

- Split the Data: Divide the data into training, testing, and validation sets to prepare for model training and evaluation.

6. Model Training

- Model Selection and Training: Train the model using XGBoost with hyperparameter optimization via Random Search or Optuna. During this step, assess feature importance and the overall model score.

7. Additional Feature Preparation

- Prepare Weather Data for Predictions: Re-read and prepare weather data, generating additional weather features if necessary.
- Generate Random Date Features: Create and save features for random dates to facilitate model predictions on unseen data.

8. Results Comparison

- Compare Predicted and Actual Data: Combine predicted values with actual values for a side-by-side comparison.
- Plotting Results: Generate graphs that compare predicted values against actual values to visualize trends and assess model performance.

### Software Dependencies

The project requires certain libraries for data manipulation, feature engineering, and model training. Please refer to requirements.txt for a full list of required packages.
Dataset

Ensure you have access to the stuttgart_23_24.csv file and other house datasets (e.g., Flo_data.csv). Place these files in the same directory as the code or update paths as needed.
Build and Test
Building the Code

- Load and Preprocess Data: The code processes time-series data, merging datasets and generating features. Run the initial scripts to load data, process missing values, and create artificial features.

- Model Training: The train_xgboost_random_search function (provided separately) performs hyperparameter tuning and trains an XGBoost model using RandomizedSearchCV.

### Contributing

Contributions are welcome! Please create a branch for new features or bug fixes and submit a pull request. Ensure all code is well-documented and tested.

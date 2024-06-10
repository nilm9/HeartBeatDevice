import pandas as pd
import numpy as np
import datetime
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Simulate a week's worth of heart rate data sampled every minute
num_days = 7
data_points_per_day = 1440  # 24 hours * 60 minutes
total_data_points = num_days * data_points_per_day

timestamps = [datetime.datetime.now() - datetime.timedelta(minutes=x) for x in range(total_data_points)]
heart_rates = np.random.randint(50, 100, size=total_data_points)  # Simulating heart rates between 50 and 100 bpm

# Create a DataFrame
data = pd.DataFrame({'timestamp': timestamps, 'heart_rate': heart_rates})
data = data.sort_values('timestamp')  # Ensure the data is sorted by timestamp

print("Initial data:")
print(data.head())

# Fill missing values (if any)
data['heart_rate'].fillna(method='ffill', inplace=True)

# Remove outliers using the IQR method
Q1 = data['heart_rate'].quantile(0.25)
Q3 = data['heart_rate'].quantile(0.75)
IQR = Q3 - Q1
data = data[(data['heart_rate'] >= Q1 - 1.5 * IQR) & (data['heart_rate'] <= Q3 + 1.5 * IQR)]

print("Data after removing outliers:")
print(data.describe())

# Calculate moving averages and standard deviations
data['rolling_mean'] = data['heart_rate'].rolling(window=60).mean()
data['rolling_std'] = data['heart_rate'].rolling(window=60).std()

# Drop NaN values resulting from rolling window calculations
data.dropna(inplace=True)

print("Data after calculating rolling mean and standard deviation:")
print(data.head())

# Normalize the heart rate data
scaler = StandardScaler()
data['normalized_heart_rate'] = scaler.fit_transform(data[['heart_rate']])

print("Data after normalization:")
print(data.head())

# Checking for missing values
missing_values = data.isnull().sum()
print("Missing values:\n", missing_values)

# Data Distribution
plt.figure(figsize=(12, 6))

# Distribution before normalization
plt.subplot(1, 2, 1)
plt.hist(data['heart_rate'], bins=50, alpha=0.7)
plt.title('Heart Rate Distribution Before Normalization')

# Distribution after normalization
plt.subplot(1, 2, 2)
plt.hist(data['normalized_heart_rate'], bins=50, alpha=0.7, color='orange')
plt.title('Heart Rate Distribution After Normalization')

plt.show()

# Checking feature engineering results
print("Feature engineering results:")
print(data[['timestamp', 'heart_rate', 'rolling_mean', 'rolling_std']].head(10))

# Optionally, save the preprocessed data for future use
data.to_csv('preprocessed_heart_rate_data.csv', index=False)

print("Preprocessed data saved to 'preprocessed_heart_rate_data.csv'")

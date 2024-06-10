import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def preprocess_data(heart_rate_data):
    """
    Preprocess the heart rate data.

    Parameters:
    heart_rate_data (pd.DataFrame): DataFrame containing raw heart rate data with columns 'timestamp' and 'heart_rate'.

    Returns:
    pd.DataFrame: Preprocessed data with additional features and normalized heart rate.
    """
    # Ensure the data is sorted by timestamp
    heart_rate_data = heart_rate_data.sort_values('timestamp')

    # Fill missing values (if any)
    heart_rate_data['heart_rate'].fillna(method='ffill', inplace=True)

    # Calculate HRV (example: standard deviation of heart rate over a rolling window)
    heart_rate_data['hrv'] = heart_rate_data['heart_rate'].rolling(window=5).std()

    # Calculate rolling mean and standard deviation of heart rate
    heart_rate_data['rolling_mean'] = heart_rate_data['heart_rate'].rolling(window=5).mean()
    heart_rate_data['rolling_std'] = heart_rate_data['heart_rate'].rolling(window=5).std()

    # Drop NaN values resulting from rolling window calculations
    heart_rate_data.dropna(inplace=True)

    # Normalize the heart rate data
    scaler = StandardScaler()
    heart_rate_data['normalized_heart_rate'] = scaler.fit_transform(heart_rate_data[['heart_rate']])
    heart_rate_data['normalized_hrv'] = scaler.fit_transform(heart_rate_data[['hrv']])
    heart_rate_data['normalized_rolling_mean'] = scaler.fit_transform(heart_rate_data[['rolling_mean']])
    heart_rate_data['normalized_rolling_std'] = scaler.fit_transform(heart_rate_data[['rolling_std']])

    return heart_rate_data

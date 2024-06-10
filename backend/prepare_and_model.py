import os
import wfdb
import pandas as pd
import numpy as np

# Path to the directory where the files are extracted
data_dir = '/Users/nilmonfortvila/Desktop/UDE/IOT/mit-bih-polysomnographic-database-1.0.0'  # Replace with the actual path

# List of all records in the directory
records = [f.split('.')[0] for f in os.listdir(data_dir) if f.endswith('.hea')]

# Initialize a list to hold all data frames
all_data_list = []


# Function to extract features and annotations
def extract_features(record, annotation):
    signals_df = pd.DataFrame(record.p_signal, columns=record.sig_name)

    # Extract heart rate (ECG signal)
    ecg_signal = signals_df['ECG'] if 'ECG' in signals_df else signals_df.iloc[:, 0]
    signals_df['heart_rate'] = ecg_signal

    # Example feature: rolling mean and standard deviation
    signals_df['rolling_mean'] = signals_df['heart_rate'].rolling(window=60).mean()
    signals_df['rolling_std'] = signals_df['heart_rate'].rolling(window=60).std()

    # Drop NaN values resulting from rolling window calculations
    signals_df.dropna(inplace=True)

    # Add annotations
    annotations = np.zeros(len(signals_df))
    for i, sample in enumerate(annotation.sample):
        if sample < len(annotations):
            try:
                annotations[sample:] = float(annotation.aux_note[i])
            except ValueError:
                # Handle non-numeric annotations
                annotations[sample:] = -1  # Assign a special value for non-numeric annotations

    signals_df['annotations'] = annotations

    return signals_df


# Process each record
for record_name in records:
    # Load the record and annotations
    record = wfdb.rdrecord(os.path.join(data_dir, record_name))
    annotation = wfdb.rdann(os.path.join(data_dir, record_name), 'st')

    # Extract features and annotations
    features_df = extract_features(record, annotation)

    # Append to the list of data frames
    all_data_list.append(features_df)

# Concatenate all data frames into one
all_data = pd.concat(all_data_list, ignore_index=True)

# Save the extracted features to a CSV file
all_data.to_csv('extracted_features.csv', index=False)

print("Feature extraction completed and saved to 'extracted_features.csv'")

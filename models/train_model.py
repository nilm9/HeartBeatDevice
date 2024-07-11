import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt

# Load a fraction of the extracted features
fraction = 0.5  # Use 10% of the data
total_rows = 12000000  # Total number of rows in the CSV (adjust if known)
rows_to_read = int(fraction * total_rows)

# Load the extracted features
all_data = pd.read_csv('../extracted_features.csv', nrows=rows_to_read)

# Normalize the heart rate data
scaler = StandardScaler()
all_data[['heart_rate', 'rolling_mean', 'rolling_std']] = scaler.fit_transform(
    all_data[['heart_rate', 'rolling_mean', 'rolling_std']])

# Prepare features and labels
X = all_data[['heart_rate', 'rolling_mean', 'rolling_std']]
y = all_data['annotations']

# Ensure annotations are numerical for the model
y = pd.factorize(y)[0]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred)}')

# Save the model
joblib.dump(model, '../backend/sleep_stage_model.pkl')

# Plot a sample of the ECG signal and the corresponding annotations
plt.figure(figsize=(12, 6))
plt.plot(all_data['heart_rate'].values[:1000], label='Heart Rate')
plt.plot(all_data['rolling_mean'].values[:1000], label='Rolling Mean')
plt.plot(all_data['rolling_std'].values[:1000], label='Rolling Std')
plt.legend()
plt.title('ECG Signal and Extracted Features')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.show()

# File: evaluate_model.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt

# Step 1: Re-evaluate the Model on Test Data
# Load the extracted features
fraction = 0.5
total_rows = 12000000
rows_to_read = int(fraction * total_rows)
all_data = pd.read_csv('/Users/nil/IOT/backend/extracted_features.csv', nrows=rows_to_read)

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

# Load the saved model
model = joblib.load('../backend/sleep_stage_model.pkl')

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Print classification report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Print confusion matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Step 2: Understand the Feature Importance
# Feature importance
importances = model.feature_importances_
feature_names = ['heart_rate', 'rolling_mean', 'rolling_std']
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.show()

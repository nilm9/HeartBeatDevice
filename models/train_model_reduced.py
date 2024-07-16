import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('/Users/nil/IOT/backend/extracted_features.csv')

# Select only the necessary columns
columns_to_keep = ['heart_rate', 'rolling_mean', 'rolling_std', 'annotations']
data = data[columns_to_keep]

# Drop rows with any missing values
data.dropna(inplace=True)

# Normalize the heart rate data
scaler = StandardScaler()
data[['heart_rate', 'rolling_mean', 'rolling_std']] = scaler.fit_transform(
    data[['heart_rate', 'rolling_mean', 'rolling_std']])

# Prepare features and labels
X = data[['heart_rate', 'rolling_mean', 'rolling_std']]
y = data['annotations']

# Ensure annotations are numerical for the model
y = pd.factorize(y)[0]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save the model
joblib.dump(model, './sleep_stage_model_trimmed.pkl')

# Plot feature importance
importances = model.feature_importances_
feature_names = ['heart_rate', 'rolling_mean', 'rolling_std']
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df['Feature'], feature_importance_df['Importance'])
plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('Feature Importance')
plt.show()

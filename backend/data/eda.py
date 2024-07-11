import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
data = pd.read_csv('../extracted_features.csv')

# Display the first few rows of the data
print("First few rows of the dataset:")
print(data.head())

# Summary statistics
print("\nSummary statistics:")
print(data.describe())

# Check for missing values
print("\nMissing values:")
print(data.isnull().sum())

# Correlation matrix
print("\nCorrelation matrix:")
corr_matrix = data.corr()
print(corr_matrix)

# Plot the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Distribution plots for key features
key_features = ['heart_rate', 'rolling_mean', 'rolling_std']

for feature in key_features:
    plt.figure(figsize=(10, 6))
    sns.histplot(data[feature].dropna(), kde=True, bins=30)
    plt.title(f'Distribution of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
    plt.show()

# Time-series plots for key features
for feature in key_features:
    plt.figure(figsize=(12, 6))
    plt.plot(data[feature], label=feature)
    plt.title(f'Time Series Plot of {feature}')
    plt.xlabel('Sample Index')
    plt.ylabel(feature)
    plt.legend()
    plt.show()

# Box plots to understand the spread and outliers
for feature in key_features:
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=data[feature])
    plt.title(f'Box Plot of {feature}')
    plt.ylabel(feature)
    plt.show()

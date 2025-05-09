import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set the style for better visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_context("talk")

# Read the dataset
print("Loading dataset...")
df = pd.read_csv('Challenger_Ranked_Games.csv')

# 1. Basic Dataset Information
print("\n1. Dataset Overview:")
print("-" * 50)
print(f"Number of games analyzed: {df.shape[0]}")
print(f"Number of features tracked: {df.shape[1]}")
print("\nFeatures in the dataset:")
print(df.columns.tolist())

# 2. Data Quality Analysis
print("\n2. Data Quality Analysis:")
print("-" * 50)
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100
missing_info = pd.DataFrame({
    'Missing Values': missing_values,
    'Percentage': missing_percentage
})
print("\nMissing Values Summary:")
print(missing_info[missing_info['Missing Values'] > 0])

# Create directory for plots
import os
if not os.path.exists('eda_plots'):
    os.makedirs('eda_plots')

# 3. Game Duration Analysis
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='gameDuration', bins=50, kde=True)
plt.title('Distribution of Game Duration')
plt.xlabel('Game Duration (minutes)')
plt.savefig('eda_plots/game_duration_distribution.png')
plt.close()

# 4. Win Rate Analysis
if 'winner' in df.columns:
    win_rate = df['winner'].value_counts(normalize=True) * 100
    plt.figure(figsize=(8, 6))
    win_rate.plot(kind='bar')
    plt.title('Win Rate Distribution')
    plt.ylabel('Percentage')
    plt.savefig('eda_plots/win_rate_distribution.png')
    plt.close()

# 5. Gold and Experience Analysis
numerical_features = df.select_dtypes(include=[np.number]).columns
gold_cols = [col for col in numerical_features if 'gold' in col.lower()]
exp_cols = [col for col in numerical_features if 'exp' in col.lower()]

if gold_cols:
    plt.figure(figsize=(12, 6))
    df[gold_cols].boxplot()
    plt.title('Gold Distribution Across Different Metrics')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('eda_plots/gold_distribution.png')
    plt.close()

# 6. Correlation Analysis
plt.figure(figsize=(15, 12))
correlation_matrix = df.select_dtypes(include=[np.number]).corr()
mask = np.triu(np.ones_like(correlation_matrix), k=1)
sns.heatmap(correlation_matrix, mask=mask, annot=False, cmap='coolwarm', center=0)
plt.title('Feature Correlation Heatmap')
plt.tight_layout()
plt.savefig('eda_plots/correlation_heatmap.png')
plt.close()

# 7. Team Performance Metrics
team_metrics = [col for col in numerical_features if 'team' in col.lower()]
if team_metrics:
    plt.figure(figsize=(15, 8))
    df[team_metrics].boxplot()
    plt.title('Team Performance Metrics Distribution')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('eda_plots/team_metrics_distribution.png')
    plt.close()

# 8. Statistical Summary
print("\n3. Statistical Summary:")
print("-" * 50)
print(df.describe())

# Save comprehensive analysis to file
print("\nSaving comprehensive analysis...")
with open('eda_plots/comprehensive_analysis.txt', 'w') as f:
    f.write("Challenger Ranked Games Analysis\n")
    f.write("=" * 50 + "\n\n")
    
    # Dataset Overview
    f.write("1. Dataset Overview\n")
    f.write("-" * 20 + "\n")
    f.write(f"Total Games Analyzed: {df.shape[0]}\n")
    f.write(f"Features Tracked: {df.shape[1]}\n\n")
    
    # Data Quality
    f.write("2. Data Quality\n")
    f.write("-" * 20 + "\n")
    f.write("Missing Values Summary:\n")
    f.write(missing_info[missing_info['Missing Values'] > 0].to_string())
    f.write("\n\n")
    
    # Statistical Summary
    f.write("3. Statistical Summary\n")
    f.write("-" * 20 + "\n")
    f.write(df.describe().to_string())
    f.write("\n\n")
    
    # Correlation Analysis
    f.write("4. Key Correlations\n")
    f.write("-" * 20 + "\n")
    high_corr = correlation_matrix[abs(correlation_matrix) > 0.7]
    f.write("Strong correlations (>0.7 or <-0.7):\n")
    for col in high_corr.columns:
        strong_corr = high_corr[col][abs(high_corr[col]) > 0.7]
        if len(strong_corr) > 1:  # More than just self-correlation
            f.write(f"\n{col} is strongly correlated with:\n")
            for other_col, corr_value in strong_corr.items():
                if col != other_col:
                    f.write(f"- {other_col}: {corr_value:.3f}\n")

print("\nEDA completed! Check the 'eda_plots' directory for visualizations and comprehensive analysis.") 
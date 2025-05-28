import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load from CSV files
# Assumes result_starrocks.csv and result_trino.csv are in the current working directory
# and have the same structure as the provided sample data

df_sr = pd.read_csv('result_starrocks.csv')
df_tr = pd.read_csv('result_trino.csv')

# Merge and cleanup
df = pd.merge(df_sr, df_tr, on='SQL', how='inner')
# Remove aggregate row if present
df = df[df['SQL'] != 'All time(ms)']

# Convert to numeric, handling OOM in Trino data
# Create clean column names for plotting
df['StarRocks'] = df['StarRocks-3.3 (ms)']
df['Trino'] = pd.to_numeric(df['Trino-475 (ms)'], errors='coerce')

# Generate query labels (Q1, Q2, ...)
df['Q'] = df['SQL'].str.replace(r'Query0*', 'Q', regex=True)

# Plotting setup
x = np.arange(len(df))
width = 0.4

plt.figure(figsize=(20, 6))
plt.bar(x - width/2, df['StarRocks'], width, label='StarRocks-3.3 (ms)', color='navy')
plt.bar(x + width/2, df['Trino'], width, label='Trino-475 (ms)', color='orange')

# Annotate OOM for Trino
max_sr = df['StarRocks'].max()
for i, val in enumerate(df['Trino']):
    if np.isnan(val):
        plt.text(i + width/2, max_sr * 0.05, 'OOM', ha='center', va='bottom', fontweight='bold')

# Labels and styling
plt.xlabel('Queries')
plt.ylabel('Execution Time (ms)')
plt.title('So sánh thời gian thực thi giữa StarRocks-3.3 và Trino-475 (Q1–Q99)')
plt.xticks(x, df['Q'], rotation=90, fontsize=6)
plt.legend()
plt.tight_layout()
plt.show()

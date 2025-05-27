import matplotlib.pyplot as plt
import numpy as np

# Data
queries = [
    "Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10",
    "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19", "Q20", "Q21", "Q22"
]
starrocks = [
    15729, 1636, 16727, 8031, 21954, 14089, 21571, 29265, 31633, 16343,
    4389, 12900, 12250, 20528, 36351, 2675, 16707, 14646, 20148, 18882, 41140, 3329
]
trino = [
    16380, 18550, 25100, 12880, 51660, 18550, 60600, 67800, np.nan, 25920,
    15030, 18920, 15610, 20720, 36100, 6530, 86400, 61800, 19930, 38340, np.nan, 9350
]

# Plot
x = np.arange(len(queries))
width = 0.35

plt.figure(figsize=(12, 6))
# Two contrasting colors: navy and orange
plt.bar(x - width/2, starrocks, width, label="StarRocks-3.3 (ms)", color='navy')
plt.bar(x + width/2, trino, width, label="Trino-475 (ms)", color='orange')

# Annotate OOM cases
for idx, val in enumerate(trino):
    if np.isnan(val):
        plt.text(x[idx] + width/2, max(starrocks) * 0.05, "OOM", ha='center', va='bottom', fontweight='bold')

plt.xlabel("Queries")
plt.ylabel("Execution Time (ms)")
plt.title("So sánh thời gian thực thi giữa StarRocks-3.3 và Trino-475")
plt.xticks(x, queries, rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

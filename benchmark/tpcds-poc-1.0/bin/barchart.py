import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# CSV data provided by user
data_starrocks = """SQL,StarRocks-3.3 (ms)
Query01,2061
Query02,2999
Query03,9219
Query04,20278
Query05,11602
Query06,7228
Query07,14110
Query08,5925
Query09,38926
Query10,3802
Query11,19620
Query12,3849
Query13,15987
Query14,64824
Query15,3532
Query16,2757
Query17,16691
Query18,6279
Query19,10342
Query20,2605
Query21,12311
Query22,48732
Query23,62911
Query24,18380
Query25,10312
Query26,3178
Query27,12889
Query28,52108
Query29,8403
Query30,1600
Query31,6066
Query32,2258
Query33,10999
Query34,5165
Query35,3694
Query36,11682
Query37,10885
Query38,4791
Query39,8399
Query40,1815
Query41,716
Query42,7370
Query43,4095
Query44,22375
Query45,2868
Query46,11461
Query47,8593
Query48,16026
Query49,13194
Query50,6280
Query51,22191
Query52,12746
Query53,11478
Query54,8796
Query55,9735
Query56,9115
Query57,4372
Query58,8405
Query59,7274
Query60,10867
Query61,17203
Query62,2469
Query63,7673
Query64,19836
Query65,14329
Query66,3878
Query67,24788
Query68,12444
Query69,2773
Query70,9467
Query71,9090
Query72,32716
Query73,3713
Query74,9111
Query75,11903
Query76,9814
Query77,9104
Query78,17521
Query79,7474
Query80,17358
Query81,2562
Query82,5093
Query83,1536
Query84,1634
Query85,5382
Query86,1947
Query87,4711
Query88,11256
Query89,7794
Query90,1941
Query91,1338
Query92,3171
Query93,8709
Query94,5420
Query95,19863
Query96,2704
Query97,6726
Query98,9968
Query99,2765
All time(ms),1111158
"""

data_trino = """SQL,Trino-475 (ms)
Query01,9180
Query02,21900
Query03,10860
Query04,OOM
Query05,27740
Query06,38160
Query07,22130
Query08,11180
Query09,36950
Query10,9410
Query11,73200
Query12,12310
Query13,61200
Query14,179400
Query15,10890
Query16,15650
Query17,24700
Query18,16440
Query19,15730
Query20,13380
Query21,83400
Query22,47460
Query23,105600
Query24,23690
Query25,27770
Query26,12650
Query27,24780
Query28,32760
Query29,20200
Query30,6710
Query31,29090
Query32,8660
Query33,16710
Query34,12980
Query35,13900
Query36,17730
Query37,16490
Query38,14660
Query39,190800
Query40,21750
Query41,1240
Query42,12120
Query43,11690
Query44,18360
Query45,14920
Query46,19500
Query47,99000
Query48,23950
Query49,18530
Query50,29290
Query51,26780
Query52,10850
Query53,17690
Query54,21150
Query55,10530
Query56,20510
Query57,63600
Query58,70200
Query59,28160
Query60,21170
Query61,25240
Query62,21250
Query63,17960
Query64,84000
Query65,24850
Query66,45230
Query67,79800
Query68,23300
Query69,10150
Query70,24420
Query71,17200
Query72,OOM
Query73,9980
Query74,51050
Query75,45460
Query76,20120
Query77,22740
Query78,54160
Query79,21820
Query80,54390
Query81,5290
Query82,18300
Query83,9840
Query84,3070
Query85,12340
Query86,4570
Query87,14390
Query88,41690
Query89,14750
Query90,7300
Query91,80070
Query92,7890
Query93,20280
Query94,9900
Query95,19580
Query96,9650
Query97,18370
Query98,21910
Query99,39760
All time(ms),2889510
"""

# Load into DataFrames
df_sr = pd.read_csv(StringIO(data_starrocks))
df_tr = pd.read_csv(StringIO(data_trino))

# Merge and cleanup
df = pd.merge(df_sr, df_tr, on='SQL', how='inner')
df = df[df['SQL'] != 'All time(ms)']

# Convert to numeric, handle OOM
df['StarRocks'] = df['StarRocks-3.3 (ms)']
df['Trino'] = pd.to_numeric(df['Trino-475 (ms)'], errors='coerce')

# Create Q labels
df['Q'] = df['SQL'].str.replace(r'Query0*', 'Q', regex=True)

# Plotting
x = np.arange(len(df))
width = 0.4

plt.figure(figsize=(20, 6))
plt.bar(x - width/2, df['StarRocks'], width, label='StarRocks-3.3 (ms)', color='navy')
plt.bar(x + width/2, df['Trino'], width, label='Trino-475 (ms)', color='orange')

# Annotate OOM
max_sr = df['StarRocks'].max()
for i, val in enumerate(df['Trino']):
    if np.isnan(val):
        plt.text(i + width/2, max_sr * 0.05, 'OOM', ha='center', va='bottom', fontweight='bold')

plt.xlabel('Queries')
plt.ylabel('Execution Time (ms)')
plt.title('So sánh thời gian thực thi giữa StarRocks-3.3 và Trino-475 (Q1–Q99)')
plt.xticks(x, df['Q'], rotation=90, fontsize=6)
plt.legend()
plt.tight_layout()
plt.show()

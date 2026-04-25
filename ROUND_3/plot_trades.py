import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PRODUCT1 = 'VEV_5400'
PRODUCT2 = 'VELVETFRUIT_EXTRACT'

FILE1 = 'ROUND_3/trades_round_3_day_0.csv'
FILE2 = 'ROUND_3/trades_round_3_day_1.csv'
FILE3 = 'ROUND_3/trades_round_3_day_2.csv'

# Load the data
data1 = pd.read_csv(FILE1, sep=';')
data2 = pd.read_csv(FILE2, sep=';')
data3 = pd.read_csv(FILE3, sep=';')

data2['timestamp'] += 1000000
data3['timestamp'] += 2000000

data = pd.concat([data1, data2, data3], ignore_index=True)

data_vouchers = data[data['symbol'] == PRODUCT1] 
data_extract = data[data['symbol'] == PRODUCT2]

# Create figure
fig, ax1 = plt.subplots()

# Left axis (VEV_5400)
ax1.plot(data_extract['timestamp'], data_extract['price'], color='red', label=PRODUCT1)
ax1.set_ylabel(PRODUCT1)
ax1.set_ylim(5190, 5320)

# Right axis (VELVETFRUIT_EXTRACT)
ax2 = ax1.twinx()
ax2.plot(data_vouchers['timestamp'], data_vouchers['price'], label=PRODUCT2)
ax2.set_ylabel(PRODUCT2)
ax2.set_ylim(0, 39)

# Shared x-axis
ax1.set_xlabel('Timestamp')
ax1.set_xlim(0, 3005000)
ax1.ticklabel_format(style='plain')

plt.title('Trades Over Time')

plt.show()
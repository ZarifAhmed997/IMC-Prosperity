import pandas as pd
import matplotlib.pyplot as plt

PRODUCT = 'VEV_4000' # Change this to the product you want to plot (VELVETFRUIT_EXTRACT, HYDROGEN_PACK, or VEV_4000)
FILE = 'ROUND_3/trades_round_3_day_0.csv'

# Load the data
data = pd.read_csv(FILE, sep=';')
data = data[data['symbol'] == PRODUCT]

# Plot the data
plt.plot(data['timestamp'], data['price'])
plt.xlabel('Timestamp')
plt.ylabel('Price')

plt.xlim(0, 1010000) 
plt.ticklabel_format(style='plain')

plt.title('Trades Over Time for ' + PRODUCT)
plt.show()
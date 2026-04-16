#Plot the deviation from the last price to the next price for a given symbol. (Seems to be fixed for data)

import matplotlib.pyplot as plt
import pandas as pd

config = {}
with open("info.txt", "r") as file:
    for line in file:
        key, value = line.strip().split('=')
        config[key] = value

TRADES = config['trades_file']
PRICES = config['prices_file']
SYMBOL = config['plot_type']
PRICE_TYPE = config['price_type']
PRODUCT_COLUMN = config['product_column']

print(f"Loading: {TRADES} | Symbol: {SYMBOL}")

file = pd.read_csv(TRADES, sep=';') 
data = file[file[PRODUCT_COLUMN] == SYMBOL].copy()

data['deviation'] = pd.to_numeric(data[PRICE_TYPE] - data[PRICE_TYPE].shift(1))

clean_data = data.groupby('timestamp')['deviation'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(clean_data['timestamp'], clean_data['deviation'], color='#2ca02c' , linestyle='none')
plt.scatter(clean_data['timestamp'], clean_data['deviation'], color='#2ca02c', s=10, alpha=0.7, label='Mean Execution Price')

plt.title(f'{SYMBOL} Deviation from last price')
plt.xlabel('Timestamp (ms)')
plt.ticklabel_format(style='plain', axis='x')
plt.ylabel('Price')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

min_deviation = data['deviation'].min()
max_deviation = data['deviation'].max()

plt.ylim(min_deviation * 2, max_deviation * 2) 
plt.xlim(0, clean_data['timestamp'].max() + 2000)

plt.tight_layout()
plt.show()
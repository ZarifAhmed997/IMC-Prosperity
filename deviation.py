#Plot the deviation from the last price to the next price for a given symbol. (Seems to be fixed for data)

import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = 'TUTORIAL_ROUND_1/trades_round_0_day_-1.csv'

SYMBOL = 'TOMATOES'

file = pd.read_csv(FILE_PATH, sep=';') 
data = file[file['symbol'] == SYMBOL].copy()

data['deviation'] = pd.to_numeric(data['price'] - data['price'].shift(1))

clean_data = data.groupby('timestamp')['deviation'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(clean_data['timestamp'], clean_data['deviation'], color='#2ca02c' , linestyle='none')
plt.scatter(clean_data['timestamp'], clean_data['deviation'], color='#2ca02c', s=10, alpha=0.7, label='Mean Execution Price')

plt.scatter(data['timestamp'], data['deviation'], color='black', s=10, alpha=0.3, label='Individual Trades')

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
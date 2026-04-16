import matplotlib.pyplot as plt
import pandas as pd

DATA = 'TUTORIAL_ROUND_1/trades_round_0_day_-1.csv'
SYMBOL = 'TOMATOES'

file = pd.read_csv(DATA, sep=';') 
data = file[file['symbol'] == SYMBOL].copy()

min_price = data['price'].min()
max_price = data['price'].max()

data['price'] = pd.to_numeric(data['price'])
clean_data = data.groupby('timestamp')['price'].mean().reset_index()

upper_data = data[data['price'] == max_price].groupby('timestamp')['price'].mean().reset_index()
lower_data = data[data['price'] == min_price].groupby('timestamp')['price'].mean().reset_index()
rest_data = data[(data['price'] != max_price) & (data['price'] != min_price)].groupby('timestamp')['price'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(clean_data['timestamp'], clean_data['price'], color='#2ca02c', linestyle='none')

plt.scatter(rest_data['timestamp'], rest_data['price'], color='black', s=10, alpha=0.7, label='Individual Trades')
plt.scatter(upper_data['timestamp'], upper_data['price'], color='red', s=20, label='Max Price')
plt.scatter(lower_data['timestamp'], lower_data['price'], color='blue', s=20, label='Min Price')

plt.title(f'{SYMBOL} Price Movement')
plt.xlabel('Timestamp (ms)')
plt.ticklabel_format(style='plain', axis='x')
plt.ylabel('Price')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

plt.ylim(min_price - 10, max_price + 10) 
plt.xlim(0, clean_data['timestamp'].max() + 2000)

plt.tight_layout()
plt.show()
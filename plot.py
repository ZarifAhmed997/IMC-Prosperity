import matplotlib.pyplot as plt
import pandas as pd

FILE_PATH = 'TUTORIAL_ROUND_1/trades_round_0_day_-1.csv'

SYMBOL = 'TOMATOES'

file = pd.read_csv(FILE_PATH, sep=';') 
data = file[file['symbol'] == SYMBOL].copy()

data['price'] = pd.to_numeric(data['price'])

clean_data = data.groupby('timestamp')['price'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(clean_data['timestamp'], clean_data['price'], label='Mean Execution Price', color='#2ca02c')

plt.scatter(data['timestamp'], data['price'], color='black', s=10, alpha=0.3, label='Individual Trades')

plt.title(f'{SYMBOL} Price Movement')
plt.xlabel('Timestamp (ms)')
plt.ticklabel_format(style='plain', axis='x')
plt.ylabel('Price')
plt.axline(None)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

min_price = data['price'].min()
max_price = data['price'].max()

plt.ylim(min_price - 10, max_price + 10) 
plt.xlim(0, clean_data['timestamp'].max() + 2000)

plt.tight_layout()
plt.show()
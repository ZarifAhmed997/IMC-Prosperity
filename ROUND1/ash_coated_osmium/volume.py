import pandas as pd
import matplotlib.pyplot as plt


config = {}
with open("/Users/zarif/Documents/IMC Prosperity/ROUND1/ash_coated_osmium/info.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line and '=' in line:
            key, value = line.split('=', 1)
            config[key] = value

# Get configuration values
PRICES = config.get('prices_file')
SYMBOL = config.get('plot_type')
PRICE_TYPE = config.get('price_type', 'price')

print(f"Loading: {PRICES} | Product: {SYMBOL} | Price Type: {PRICE_TYPE}")

data = pd.read_csv(PRICES, sep=';')
product_data = data[data['product'] == SYMBOL].copy()
product_data = product_data.sort_values('timestamp')
ask_volume = product_data['ask_volume_1']
bid_volume = product_data['bid_volume_1']

plt.figure(figsize=(12, 6))
plt.scatter(product_data['timestamp'], ask_volume, color='red', s=5, alpha=0.7, label='Ask Volume')
plt.scatter(product_data['timestamp'], bid_volume, color='blue', s=5, alpha=0.7, label='Bid Volume')
plt.title(f'{SYMBOL} Volume Over Time')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Volume')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.ticklabel_format(style='plain', axis='x')
plt.legend()
plt.tight_layout()
plt.ylim(0, max(ask_volume.max(), bid_volume.max()) * 1.1)
plt.xlim(0, product_data['timestamp'].max() + 2000)

plt.show()

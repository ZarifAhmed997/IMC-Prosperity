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
spread = product_data['ask_price_1'] - product_data['bid_price_1']

plt.figure(figsize=(12, 6))
plt.plot(product_data['timestamp'], spread, color='purple', alpha=0.7, linestyle='none')
plt.scatter(product_data['timestamp'], spread, color='purple', s=5, alpha=0.7, label='Spread (Ask - Bid)')
plt.title(f'{SYMBOL} Spread Over Time')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Spread')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.ticklabel_format(style='plain', axis='x')
plt.legend()
plt.tight_layout()
plt.ylim(-spread.min() * 2, spread.max() * 2)
plt.xlim(0, product_data['timestamp'].max() + 2000)

plt.show()

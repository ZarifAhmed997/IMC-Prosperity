import matplotlib.pyplot as plt
import pandas as pd

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

plt.figure(figsize=(12, 6))
plt.plot(product_data['timestamp'], product_data['bid_price_1'], label='Bid (Buy)', color='blue', alpha=0.5)
plt.plot(product_data['timestamp'], product_data['ask_price_1'], label='Ask (Sell)', color='red', alpha=0.5)

plt.title(f'{SYMBOL} - {PRICE_TYPE.replace("_", " ").title()}')
plt.xlabel('Timestamp (ms)')
plt.ylabel(f'{PRICE_TYPE.replace("_", " ").title()}')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.ticklabel_format(style='plain', axis='x')
plt.tight_layout()
plt.show()
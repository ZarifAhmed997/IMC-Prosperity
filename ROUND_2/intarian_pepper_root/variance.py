
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

config = {}
with open("/Users/zarif/Documents/IMC Prosperity/ROUND_2/intarian_pepper_root/info.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line and '=' in line:
            key, value = line.split('=', 1)
            config[key] = value

# Get configuration values
PRICES = config.get('prices_file')
SYMBOL = config.get('plot_type')  
PRICE_TYPE = config.get('price_type', 'mid_price')

# Trend line parameters
INITIAL_PRICE = 13000
SLOPE = 0.001

print(f"Loading: {PRICES} | Product: {SYMBOL} | Price Type: {PRICE_TYPE}")

data = pd.read_csv(PRICES, sep=';')
product_data = data[data['product'] == SYMBOL].copy()
product_data = product_data[product_data[PRICE_TYPE] != 0]
product_data = product_data.sort_values('timestamp')

product_data['trend_price'] = INITIAL_PRICE + (SLOPE * product_data['timestamp'])
product_data['deviation'] = product_data[PRICE_TYPE] - product_data['trend_price']

# Calculate statistics
variance = product_data['deviation'].var()
std_dev = product_data['deviation'].std()
mean_dev = product_data['deviation'].mean()

print(f"Trend Line: {INITIAL_PRICE} + {SLOPE} * timestamp")
print(f"Mean Deviation: {mean_dev:.4f}")
print(f"Std Deviation: {std_dev:.4f}")
print(f"Variance: {variance:.4f}")
print(f"Min Deviation: {product_data['deviation'].min():.4f}")
print(f"Max Deviation: {product_data['deviation'].max():.4f}")

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.scatter(product_data['timestamp'], product_data[PRICE_TYPE], label='Actual Price', color='blue', s=5, alpha=0.6)
plt.plot(product_data['timestamp'], product_data['trend_price'], label='Trend Line (slope=0.001)', color='red', linewidth=1)
plt.title(f'{SYMBOL} - Price vs Trend Line')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, product_data['timestamp'].max() + 2000)

plt.subplot(1, 2, 2)
plt.scatter(product_data['timestamp'], product_data['deviation'], color='purple', s=10, alpha=0.6)
plt.axhline(y=0, color='red', linestyle='--', linewidth=1, label='Zero Deviation')
plt.title(f'Deviation from Trend Line')
plt.xlabel('Timestamp (ms)')
plt.ylabel('Deviation (Price - Trend)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xlim(0, product_data['timestamp'].max() + 2000)

plt.ticklabel_format(style='plain', axis='x')
plt.tight_layout()
plt.show()
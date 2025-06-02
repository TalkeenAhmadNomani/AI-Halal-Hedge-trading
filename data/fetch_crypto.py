from pycoingecko import CoinGeckoAPI
import pandas as pd

# Initialize the API
cg = CoinGeckoAPI()

# List of coin IDs as used by CoinGecko
coins = ['bitcoin', 'ethereum', 'cardano']  # Use lowercase IDs

# Fetch market data for each coin
coin_data = []

for coin in coins:
    data = cg.get_coin_market_chart_by_id(id=coin, vs_currency='usd', days=30)
    prices = data['prices']
    
    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['coin'] = coin
    coin_data.append(df)

# Combine all coins into one DataFrame
combined_df = pd.concat(coin_data)

# Save to CSV
combined_df.to_csv('./csv/crypto_prices.csv', index=False)

# Display top rows
print(combined_df.head())

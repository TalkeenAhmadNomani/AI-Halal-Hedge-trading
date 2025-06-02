import pandas as pd
import yfinance as yf
import os
import time

# Step 1: Create output folders
os.makedirs("all_stocks_data", exist_ok=True)
os.makedirs("combined_data", exist_ok=True)

# ✅ Step 2: Load correct S&P 500 tickers
url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
tickers_df = pd.read_csv(url)

print("Columns found in CSV:", tickers_df.columns)

# Get ticker symbols
if 'Symbol' in tickers_df.columns:
    tickers = tickers_df['Symbol'].dropna().unique().tolist()
else:
    raise KeyError("❌ 'Symbol' column not found in the ticker source.")

# Optional: limit for testing
# tickers = tickers[:10]

# Step 3: Set date range
start_date = "2024-01-01"
end_date = "2024-12-31"

# Step 4: Download data
combined_df_list = []

for ticker in tickers:
    try:
        print(f"Downloading: {ticker}")
        df = yf.download(ticker, start=start_date, end=end_date)

        if not df.empty:
            df['Ticker'] = ticker
            df.to_csv(f"all_stocks_data/{ticker}.csv")
            combined_df_list.append(df)

        time.sleep(1)
    except Exception as e:
        print(f"⚠️ Error with {ticker}: {e}")

# Step 5: Save combined file
if combined_df_list:
    combined_df = pd.concat(combined_df_list)
    combined_df.to_csv("combined_data/all_stocks_combined.csv", index=False)
    print("✅ Combined CSV saved at 'combined_data/all_stocks_combined.csv'")
else:
    print("⚠️ No stock data was saved.")

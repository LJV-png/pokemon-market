import os
import pandas as pd
from datetime import date
import random
import requests

# CSV location
csv_path = "docs/market.csv"
os.makedirs("docs", exist_ok=True)

# Load existing CSV
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    df = pd.DataFrame(columns=["date", "index"])

# --- Step 1: TCGPlayer real data ---
TCGPLAYER_KEY = os.environ.get("TCGPLAYER_KEY")

def get_tcgplayer_avg_price():
    url = "https://api.tcgplayer.com/v1.39.0/catalog/products"
    headers = {"Authorization": f"bearer {TCGPLAYER_KEY}"}
    params = {"categoryId": "3", "productTypes": "Booster"}  # Pokémon booster packs
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        prices = [float(p["marketPrice"]) for p in data.get("results", []) if p.get("marketPrice")]
        if prices:
            return sum(prices)/len(prices)
        return 0
    except Exception as e:
        print("TCGPlayer fetch error:", e)
        return 0

# --- Step 2: Mock eBay price for now ---
def get_mock_ebay_price():
    last_value = df["index"].iloc[-1] if not df.empty else 100
    return last_value + random.randint(-5, 5)

# --- Step 3: Compute index ---
tcg_price = get_tcgplayer_avg_price()
ebay_price = get_mock_ebay_price()

index_value = round((tcg_price + ebay_price) / 2, 2) if (tcg_price + ebay_price) > 0 else 100

# Append new row
today = date.today().isoformat()
df.loc[len(df)] = [today, index_value]

# Save CSV
df.to_csv(csv_path, index=False)
print(f"Updated {csv_path} with index {index_value} for {today}")

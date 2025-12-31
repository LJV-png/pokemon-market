import pandas as pd
from datetime import datetime
import os
import random

# =========================
# CONFIG
# =========================
OUTPUT_CSV = "docs/market.csv"

BASE_INDEX = 100
MAX_DAILY_MOVE = 3  # % swing cap

# =========================
# LOAD EXISTING DATA
# =========================
if os.path.exists(OUTPUT_CSV):
    df = pd.read_csv(OUTPUT_CSV)
else:
    df = pd.DataFrame(columns=["date", "index"])

# =========================
# MOCK MARKET LOGIC
# (matches how real data will behave)
# =========================
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

if df.empty:
    new_value = BASE_INDEX
else:
    last = df["index"].iloc[-1]
    pct_move = random.uniform(-MAX_DAILY_MOVE, MAX_DAILY_MOVE)
    new_value = round(last * (1 + pct_move / 100), 2)

# =========================
# APPEND ROW
# =========================
df.loc[len(df)] = [now, new_value]

df.to_csv(OUTPUT_CSV, index=False)

print(f"Index updated → {new_value}")

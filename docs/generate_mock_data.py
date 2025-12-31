import pandas as pd
from datetime import date, timedelta
import random

csv_path = "docs/market.csv"

# create 30 days of mock data
rows = []
value = 100
start_date = date.today() - timedelta(days=29)
for i in range(30):
    rows.append({"date": (start_date + timedelta(days=i)).isoformat(),
                 "index": value})
    value += random.randint(-5, 5)

df = pd.DataFrame(rows)
df.to_csv(csv_path, index=False)
print("CSV generated with 30 days of data")

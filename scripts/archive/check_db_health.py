import pandas as pd

df = pd.read_excel('prizma-urunler-guncel.xlsx')

print("--- Data Health Check ---")
print(f"Total Rows: {len(df)}")

missing_labels = df[df['label'].isna() | (df['label'] == '')]
print(f"Missing Labels: {len(missing_labels)}")

missing_prices = df[df['price1'].isna() | (df['price1'] == '')]
print(f"Missing price1: {len(missing_prices)}")

missing_category = df[df['category'].isna() | (df['category'] == '')]
print(f"Missing Category: {len(missing_category)}")

missing_brand = df[df['brand'].isna() | (df['brand'] == '')]
print(f"Missing Brand: {len(missing_brand)}")

duplicate_stoks = df[df.duplicated(subset=['stockCode'], keep=False)]
duplicate_stoks = duplicate_stoks[duplicate_stoks['stockCode'].notna()]
print(f"Duplicate Valid StockCodes: {len(duplicate_stoks)}")

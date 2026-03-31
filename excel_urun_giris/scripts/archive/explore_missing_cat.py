import pandas as pd

df = pd.read_excel('prizma-urunler-guncel.xlsx')

missing_category = df[df['category'].isna() | (df['category'] == '')]
print("--- Products with missing category ---")
for idx, row in missing_category.head(30).iterrows():
    print(f"Brand: {row.get('brand')}, Label: {row.get('label')}")
print(f"Showing exactly 30 out of {len(missing_category)}")

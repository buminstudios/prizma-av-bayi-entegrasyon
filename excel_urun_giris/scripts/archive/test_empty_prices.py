import pandas as pd
df = pd.read_excel('prizma-urunler-guncel.xlsx')
empty = df[df['price1'].isna() | (df['price1'] == 0) | (df['price1'] == 0.0)].copy()
empty['brand'] = empty['label'].apply(lambda x: str(x).split(' ')[0] if pd.notna(x) else '')
counts = empty['brand'].value_counts()
print(counts.head(20))

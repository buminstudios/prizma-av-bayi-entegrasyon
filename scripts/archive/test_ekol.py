import pandas as pd
import sys

try:
    df = pd.read_excel('ürünler fiyatlar/EKOL KURUSIKI.xls')
    for idx, row in df.iterrows():
        if idx > 20: break
        print(idx, list(row.values[:4]))
except Exception as e:
    print('Error:', e)

import pandas as pd
import sys
try:
    df = pd.read_excel('ürünler fiyatlar/ASG FİYAT LİSTESİ 26.12.2025.xlsx')
    for idx, row in df.iterrows():
        if idx > 30: break
        print(idx, list(row.values))
except Exception as e:
    print('Error:', e)

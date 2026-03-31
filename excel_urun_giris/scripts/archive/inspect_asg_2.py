import pandas as pd
df = pd.read_excel('ürünler fiyatlar/ASG FİYAT LİSTESİ 26.12.2025.xlsx', skiprows=3) # Changed to 3
print("columns:", df.columns.tolist())
print(df.head())

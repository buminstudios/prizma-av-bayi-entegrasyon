import pandas as pd

asg_file = "ürünler fiyatlar/ASG FİYAT LİSTESİ 26.12.2025.xlsx"
df = pd.read_excel(asg_file, engine='openpyxl')
print("ASG Excel Columns:", df.columns.tolist())
print(df.head())

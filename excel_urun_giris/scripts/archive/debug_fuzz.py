import pandas as pd
from thefuzz import process, fuzz

df = pd.read_excel('prizma-urunler-guncel.xlsx', nrows=4080)
existing_names = df['label'].dropna().astype(str).tolist()

match_name = "Stil Crin 6.35mm ALÜMİNYUM BAKIM Set (HAZNELİ)"
match_result = process.extractOne(match_name, existing_names, scorer=fuzz.token_sort_ratio)
print(f"Match: {match_result}")

match_name2 = "Sig Sauer 1911 TACOPS AIRSOFT TABANCA"
match_result2 = process.extractOne(match_name2, existing_names, scorer=fuzz.token_sort_ratio)
print(f"Match2: {match_result2}")

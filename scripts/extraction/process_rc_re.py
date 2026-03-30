import pandas as pd
from thefuzz import process, fuzz
import re

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# 1. Truncate the file to remove the previous 22 incorrectly added RC items
df_main = pd.read_excel(FILE_PATH)

# Find the exact index where my previous script started appending (it's the first new RC item I added)
# "RC 2 COMP.LINE 28 GR FİŞEK" was my first new product.
first_new_idx = df_main[df_main['label'] == 'RC 2 COMP.LINE 28 GR FİŞEK'].index.min()
if pd.notna(first_new_idx):
    print(f"Truncating database at index {first_new_idx} to remove duplicates.")
    df_main = df_main.iloc[:int(first_new_idx)]

rc_items = [
    {"name": "RC 2 COMP.LINE 28 GR", "price": 23.150, "box": 25},
    {"name": "RC 30 CACCIA 30 GR", "price": 25.150, "box": 25},
    {"name": "RC 31 TITANO 31 GR", "price": 25.425, "box": 25},
    {"name": "RC 32 CACCIA 32 GR", "price": 26.250, "box": 25},
    {"name": "RC 1 CACCIA 33 GR", "price": 26.500, "box": 25},
    {"name": "RC SIPE 32 GR", "price": 34.600, "box": 25},
    {"name": "RC S4 SPECIAL 33 GR", "price": 34.900, "box": 25},
    {"name": "RC 2 CACCIA 34 GR", "price": 27.500, "box": 25},
    {"name": "RC2 KAĞIT KOVAN KEÇE TAPA 32 GR", "price": 33.800, "box": 25},
    {"name": "RC 20 KAL SIPE 25 GR", "price": 28.400, "box": 25},
    {"name": "RC 20 SIPE KEÇE TAPA 26 GR", "price": 29.000, "box": 25},
    {"name": "RC 20T3 28 GR", "price": 27.500, "box": 25},
    {"name": "RC CAMOUFLAGE 34 GR", "price": 31.350, "box": 25},
    {"name": "RC 1 GAME LINE 36 GR", "price": 31.350, "box": 25},
    {"name": "RC 3 DISPERSANTE 33 GR", "price": 30.150, "box": 25},
    {"name": "RC 4 DISPERSANTE 34 GR", "price": 33.280, "box": 25},
    {"name": "RC 2 COM.LINE TRAP 24 GR", "price": 22.280, "box": 25},
    {"name": "RC 2 COM.LINE SKEET 24 GR", "price": 23.000, "box": 25},
    {"name": "RC 4 HYPERFAST 24 GR", "price": 29.325, "box": 25},
    {"name": "RC 4 CHAMPION EXCELLENCE 24 GR", "price": 29.225, "box": 25},
    {"name": "RC RED SHOT SUP.NIK 24 GR", "price": 29.750, "box": 25},
    {"name": "RC 4 ŞEVROTTİN BUCKSHOT", "price": 52.750, "box": 10},
    {"name": "RC TEK KURŞUN 32 GR PALLA", "price": 67.500, "box": 10},
]

def clean_name(n):
    n = str(n).upper()
    n = re.sub(r'AV FİŞEĞİ|12 CAL\.|12 CAL|20 CAL\.|20 CAL|FİŞEK|GR\.|GR|,|:', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

existing_series = df_main['label'].dropna()
existing_names = existing_series.tolist()
# Create a dict of simplified db name to original db name so we can map it back
db_map = {clean_name(name): name for name in existing_names if 'RC' in str(name).upper()}

matched_count = 0
new_rows = []

for item in rc_items:
    ext_name_clean = clean_name(item['name'])
    final_price = round((item['price'] * item['box'] * 1.35) / 1.20, 2)
    
    # Fuzzy match with token_set_ratio on cleaned strings
    match_result = process.extractOne(ext_name_clean, list(db_map.keys()), scorer=fuzz.token_set_ratio)
    
    if match_result and match_result[1] >= 85: # Increased safety due to cleaning
        best_clean = match_result[0]
        original_db_name = db_map[best_clean]
        
        df_main.loc[df_main['label'] == original_db_name, 'price1'] = final_price
        df_main.loc[df_main['label'] == original_db_name, 'currencyAbbr'] = 'TL'
        df_main.loc[df_main['label'] == original_db_name, 'brand'] = 'RC'
        matched_count += 1
        print(f"Matched: '{item['name']}' -> '{original_db_name}' (Score: {match_result[1]})")
    else:
        inferred_main_cat = "AV FİŞEKLERİ"
        new_rows.append({
            'label': item['name'],
            'price1': final_price,
            'currencyAbbr': 'TL',
            'status': 1,
            'brand': 'RC',
            'mainCategory': inferred_main_cat,
            'category': "RC Fişekler",
            'subCategory': ""
        })
        print(f"NEW ADD: '{item['name']}' (Best match was '{match_result[0]}' score {match_result[1]} if any)")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

df_main.to_excel(FILE_PATH, index=False)
print(f"Matched & Updated: {matched_count}")
print(f"Added as new: {len(new_rows)}")

import pandas as pd
from thefuzz import process, fuzz
import os

OUTPUT_EXCEL = 'prizma-urunler-guncel.xlsx'

# Data extracted perfectly from the image "WhatsApp Image 2026-03-27 at 18.22.50.jpeg"
# Name prefix 'Ekol' is added to help with fuzzy matching.
ekol_products = {
    "Ekol ES 55": 2400.00,
    "Ekol ES 66": 3120.00,
    "Ekol ES 66 C": 3120.00,
    "Ekol ES P66": 2700.00,
    "Ekol ES P66 C": 2580.00,
    "Ekol ES P92": 3060.00,
    "Ekol ES P92 B": 3840.00,
    "Ekol ES P95 B": 4560.00,
    "Ekol ES 1911": 3840.00,
    "Ekol ES 1911 C": 3840.00,
    "Ekol FOWLER": 2160.00,
    "Ekol HAVALI TÜFEK MAJÖR": 3300.00,
    "Ekol ULTIMATE": 3300.00,
    "Ekol THUNDER": 3480.00,
    "Ekol THUNDER-M": 3600.00,
    "Ekol ULTIMATE-F": 3720.00,
    "Ekol MAJÖR-F": 3720.00,
    "Ekol THUNDER-F": 3960.00,
    "Ekol THUNDER-FM": 4080.00,
    "Ekol AK": 4200.00,
    "Ekol AKL": 4200.00,
    "Ekol M": 4080.00,
    "Ekol ML": 4080.00,
    "Ekol MS": 4080.00,
    "Ekol MC": 4080.00,
    "Ekol PCP 1": 10200.00,
    "Ekol PCP 2": 10200.00,
    "Ekol PCP 3": 10200.00,
    "Ekol PCP 4": 10200.00,
    "Ekol ALP": 2916.00,
    "Ekol ALP-2": 2916.00,
    "Ekol ALPER": 2916.00,
    "Ekol ARAS MAGNUM": 3240.00,
    "Ekol ARAS COMPACT": 3240.00,
    "Ekol BOTAN": 2268.00,
    "Ekol DİCLE": 3240.00,
    "Ekol FIRAT COMPACT": 3240.00,
    "Ekol FIRAT MAGNUM": 3240.00,
    "Ekol FIRAT P92": 3240.00,
    "Ekol FIRAT PA92": 3240.00,
    "Ekol FIRAT PB92": 3240.00,
    "Ekol FIRAT PC92": 3240.00,
    "Ekol GEDİZ": 3412.80,
    "Ekol KURA": 2376.00,
    "Ekol LADY": 2433.60,
    "Ekol MAJAROV": 2678.40,
    "Ekol KURUSIKI MAJÖR": 2433.60,
    "Ekol NİG 211": 3456.00,
    "Ekol P29": 2736.00,
    "Ekol P29 REV 2": 2916.00,
    "Ekol SAVA": 3024.00,
    "Ekol SPECIAL 99": 2736.00,
    "Ekol SPECIAL 99 REV 2": 2916.00,
    "Ekol TİSA": 2160.00,
    "Ekol TUNA": 1944.00,
    "Ekol VOLGA": 2088.00,
    "Ekol ARDA": 2592.00,
    "Ekol VIPER LITE": 3096.00,
    "Ekol VIPER 2,5": 3168.00,
    "Ekol VIPER 3": 3168.00,
    "Ekol VIPER 4,5": 3240.00,
    "Ekol VIPER 6": 3312.00
}

# The user wants prices to be increased by 35% from the list.
# Then apply the general KDV rule: KDV hariç (/ 1.20) because site adds it mathematically.
df_main = pd.read_excel(OUTPUT_EXCEL)
existing_names = df_main['label'].dropna().astype(str).tolist()

matched_count = 0
new_rows = []
unmatched_items = []

for ext_name, original_price in ekol_products.items():
    # 1. KDV dahil listeden %35 zam yap
    zamli_fiyat = original_price * 1.35
    # 2. Siteye KDV hariç girileceği için / 1.20 böl
    kdv_haric_fiyat = zamli_fiyat / 1.20
    final_price = round(kdv_haric_fiyat, 2)
    
    match_result = process.extractOne(ext_name, existing_names, scorer=fuzz.token_sort_ratio)
    
    if match_result:
        best_match_name, score = match_result[0], match_result[1]
        if score >= 85:
            # Güncelle
            df_main.loc[df_main['label'] == best_match_name, 'price1'] = final_price
            df_main.loc[df_main['label'] == best_match_name, 'currencyAbbr'] = 'TL'
            matched_count += 1
        else:
            new_rows.append({
                'label': ext_name,
                'price1': final_price,
                'currencyAbbr': 'TL',
                'status': 1
            })
            unmatched_items.append({"name": ext_name, "price": final_price, "currency": "TL"})
    else:
        new_rows.append({
            'label': ext_name,
            'price1': final_price,
            'currencyAbbr': 'TL',
            'status': 1
        })
        unmatched_items.append({"name": ext_name, "price": final_price, "currency": "TL"})

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

df_main.to_excel(OUTPUT_EXCEL, index=False)

print(f"Görselden okunan ürün sayısı: {len(ekol_products)}")
print(f"Eşleşip güncellenen: {matched_count}")
print(f"Yeni satır olarak eklenen: {len(new_rows)}")

# Update the log
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n- WhatsApp Görselinden (Ekol Voltran) **{len(ekol_products)}** ürün işlendi. Liste fiyatına **%35 zam** yapıldı ve KDV düşülüp Excel'e eklendi.\n")

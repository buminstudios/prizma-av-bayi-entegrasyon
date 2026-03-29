import pandas as pd
from thefuzz import process, fuzz
import os
import datetime

OUTPUT_EXCEL = 'prizma-urunler-guncel.xlsx'
UNMATCHED_CSV = 'eslesmeyenler.csv'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# TEPFS YOK - TAMAMI TOPTAN NET LİSTE
batch_1_items = [
    # Elbiseler
    {"name": "SAZ DESEN -30 TAKIM M-L-XL-XXL", "price": 2500.00, "currency": "TL", "tepfs": False},
    {"name": "KOYU SAZ DESEN -30 TAKIM M-L-XL-XXL", "price": 2500.00, "currency": "TL", "tepfs": False},
    {"name": "MEŞE DESEN TAKIM M-L-XL-XXL", "price": 2500.00, "currency": "TL", "tepfs": False},
    
    # Dürbünler
    {"name": "100X100 COMET EL DÜRBÜNÜ", "price": 12.20, "currency": "USD", "tepfs": False},
    {"name": "8X40 COMET EL DÜRBÜNÜ", "price": 31.50, "currency": "USD", "tepfs": False},
    {"name": "7X50 COMET EL DÜRBÜNÜ", "price": 27.50, "currency": "USD", "tepfs": False},
    {"name": "10-30X50 COMET EL DÜRBÜNÜ", "price": 38.30, "currency": "USD", "tepfs": False},
    {"name": "20X50 COMET EL DÜRBÜNÜ", "price": 35.60, "currency": "USD", "tepfs": False},
    {"name": "3-9X42 COMET TÜFEK DÜRBÜNÜ", "price": 36.00, "currency": "USD", "tepfs": False},
    {"name": "3-9X42 EG COMET TÜFEK DÜRBÜNÜ", "price": 39.80, "currency": "USD", "tepfs": False},
    {"name": "3-9X50 COMET TÜFEK DÜRBÜNÜ", "price": 41.50, "currency": "USD", "tepfs": False},
    {"name": "3-9X50 EG COMET TÜFEK DÜRBÜNÜ", "price": 46.00, "currency": "USD", "tepfs": False},
    {"name": "3-9X32 EG COMET TÜFEK DÜRBÜNÜ", "price": 39.50, "currency": "USD", "tepfs": False},
    {"name": "4X20 RIFLE SCOPE TÜFEK DÜRBÜNÜ", "price": 7.50, "currency": "USD", "tepfs": False},

    # Özkursan Fişek
    {"name": "ÖZK 12 CAL SES FİŞEĞİ", "price": 12.80, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL BILDIRCIN ÖZEL KEÇE DİZAYN BİOR", "price": 13.00, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL ÇULLUK ÖZEL KEÇE DİZAYN BİOR", "price": 13.78, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL 33 GR DİSPERSANTE", "price": 25.00, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL 33 G TAVŞAN ÖZEL", "price": 14.98, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL 33 G ÖRDEK ÖZEL", "price": 14.98, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL 33 G KEKLİK ÖZEL", "price": 14.98, "currency": "TL", "tepfs": False},
    {"name": "COM 12 CAL ÜVEYİK ÖZEL", "price": 12.50, "currency": "TL", "tepfs": False},
    {"name": "COM 12 CAL BILDIRCIN", "price": 12.50, "currency": "TL", "tepfs": False},
    {"name": "COM 12 CAL KOD-34 TAVŞAN ÖZEL", "price": 12.50, "currency": "TL", "tepfs": False},
    {"name": "COM 12 CAL KOD-34 ÖRDEK ÖZEL", "price": 12.50, "currency": "TL", "tepfs": False},
    {"name": "CLK 12 CAL 24 GR TRAP STEEL (70 MM)", "price": 12.50, "currency": "TL", "tepfs": False},
    {"name": "CLK 12 CAL BILDIRCIN STEEL (70 MM)", "price": 12.50, "currency": "TL", "tepfs": False},
    {"name": "CODEX BILDIRCIN ( KEÇE DİZAYN )", "price": 13.00, "currency": "TL", "tepfs": False},
    {"name": "CODEX 24 GR TRAP", "price": 13.48, "currency": "TL", "tepfs": False},
    {"name": "CODEX 24 GR SKEET", "price": 13.48, "currency": "TL", "tepfs": False},
    {"name": "CODEX 28 GR KEÇE DİZAYN", "price": 14.28, "currency": "TL", "tepfs": False},
    {"name": "CODEX 30 GR KEÇE DİZAYN", "price": 14.58, "currency": "TL", "tepfs": False},
    {"name": "CODEX 32 GR KEÇE DİZAYN", "price": 14.78, "currency": "TL", "tepfs": False},
    {"name": "CODEX 34 GR KEÇE DİZAYN", "price": 14.98, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL KURŞUN ETNA POWER", "price": 18.00, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL KURŞUN CODEX COMBO", "price": 18.50, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL KURŞUN TURNA", "price": 20.00, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL KURŞUN SNİPER", "price": 20.00, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 12 CAL KURŞUN HIZLI", "price": 21.00, "currency": "TL", "tepfs": False},
    {"name": "ÖZKURSAN MANEVRA FİŞEĞİ", "price": 4.40, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 5700 9 MM BEYAZ 5700", "price": 3.35, "currency": "TL", "tepfs": False},
    {"name": "ÖZK 5701 9 MM SARI 5701", "price": 3.31, "currency": "TL", "tepfs": False},
    {"name": "CDX7701 9 MM SARI LAGANT (500 BAR)", "price": 3.20, "currency": "TL", "tepfs": False},
    {"name": "CK.9 ÖZKURSAN CK9 SES MERMİSİ", "price": 3.20, "currency": "TL", "tepfs": False},

    # Meca Fişek
    {"name": "GECO SES MERMİSİ SARI", "price": 4.54, "currency": "TL", "tepfs": False},
    {"name": "MECA SÜPER TRAP 24 GR", "price": 15.00, "currency": "TL", "tepfs": False},
    {"name": "MECA SÜPER SKEET 24 GR", "price": 15.00, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 28 GR POWER", "price": 16.20, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 28 GR BİOR", "price": 17.10, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 30 GR POWER", "price": 17.10, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 30 GR BİOR", "price": 17.40, "currency": "TL", "tepfs": False},
    {"name": "MECA MASTER HUNTİNG 32 GR", "price": 17.70, "currency": "TL", "tepfs": False},
    {"name": "MECA SPECİAL HUNTİNG 33 GR BİOR", "price": 18.60, "currency": "TL", "tepfs": False},
    {"name": "MECA PRO HUNTİNG 34 GR", "price": 18.00, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 36 GR", "price": 19.80, "currency": "TL", "tepfs": False},
    {"name": "MECA HUNTER QUAİL (BILDIRCIN ÖZEL) 26 GR", "price": 16.20, "currency": "TL", "tepfs": False},
    {"name": "MECA HUNTER DOVE (ÜVEYİK ÖZEL) 29 GR", "price": 17.40, "currency": "TL", "tepfs": False},
    {"name": "MECA HUNTER BECASİN (ÇULLUK ÖZEL) 31 GR", "price": 17.70, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 16 CAL", "price": 18.00, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 20 CAL 25 GR", "price": 18.00, "currency": "TL", "tepfs": False},
    {"name": "MECA SPEED HUNTİNG 20 CAL 28 GR", "price": 18.00, "currency": "TL", "tepfs": False},
    {"name": "MECA RİFLED KURŞUN 16 CAL", "price": 25.20, "currency": "TL", "tepfs": False},
    {"name": "MECA RİFLED KURŞUN 20 CAL", "price": 25.20, "currency": "TL", "tepfs": False},
    {"name": "MECA ŞEVROTİN 16 CAL", "price": 22.20, "currency": "TL", "tepfs": False},
    {"name": "MECA ŞEVROTİN 20 CAL", "price": 22.20, "currency": "TL", "tepfs": False},
    {"name": "MECA RİFLED KURŞUN", "price": 25.20, "currency": "TL", "tepfs": False},
    {"name": "MECA EXTRA KURŞUN", "price": 28.80, "currency": "TL", "tepfs": False},
    {"name": "MECA DOUBLE KURŞUN", "price": 27.60, "currency": "TL", "tepfs": False},
    {"name": "MECA MONO BALL KURŞUN 34 GR", "price": 25.20, "currency": "TL", "tepfs": False},
    {"name": "MECA ŞEVROTİN", "price": 22.20, "currency": "TL", "tepfs": False},
    {"name": "MECA GECO RED STAR", "price": 35.40, "currency": "TL", "tepfs": False},
    {"name": "MECA GECO SABOT KURŞUN", "price": 43.80, "currency": "TL", "tepfs": False}
]

df_main = pd.read_excel(OUTPUT_EXCEL)
existing_names = df_main['label'].dropna().astype(str).tolist()

matched_count = 0
multi_matched_count = 0
new_rows = []
unmatched_items = []
price_drop_warnings = []

print("Adım 1: Chat'ten yollanan 4 görsel işleniyor...")

for item in batch_1_items:
    ext_name = item['name']
    original_price = item['price']
    
    if item['tepfs']:
        final_price = round(original_price / 1.20, 2)
    else:
        final_price = round((original_price * 1.35) / 1.20, 2)
        
    match_result = process.extractOne(ext_name, existing_names, scorer=fuzz.token_sort_ratio)
    
    if match_result and match_result[1] >= 85:
        best_match_name = match_result[0]
        try:
            current_price_raw = df_main.loc[df_main['label'] == best_match_name, 'price1'].values[0]
            current_price = float(str(current_price_raw).replace(',', '.'))
        except:
            current_price = 0.0

        if current_price > 0 and final_price < current_price:
            price_drop_warnings.append(f"- **DÜŞÜK FİYAT ENGELLENDİ**: '{ext_name}' (Mevcut: {current_price}, Yeni: {final_price}).")
        else:
            df_main.loc[df_main['label'] == best_match_name, 'price1'] = final_price
            df_main.loc[df_main['label'] == best_match_name, 'currencyAbbr'] = item['currency']
            matched_count += 1
            
    else:
        set_matches = process.extract(ext_name, existing_names, limit=20, scorer=fuzz.token_set_ratio)
        valid_set_matches = [m for m in set_matches if m[1] >= 90]
        
        if valid_set_matches and len(ext_name) >= 5:
            # Multi-Update
            for m in valid_set_matches:
                db_name = m[0]
                try:
                    current_price_raw = df_main.loc[df_main['label'] == db_name, 'price1'].values[0]
                    current_price = float(str(current_price_raw).replace(',', '.'))
                except:
                    current_price = 0.0

                if current_price > 0 and final_price < current_price:
                    price_drop_warnings.append(f"- **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: '{ext_name}' (İdeasoft: {db_name}) Mevcut: {current_price}, Yeni: {final_price}.")
                else:
                    df_main.loc[df_main['label'] == db_name, 'price1'] = final_price
                    df_main.loc[df_main['label'] == db_name, 'currencyAbbr'] = item['currency']
                    multi_matched_count += 1
        else:
            inferred_main_cat = "KATEGORİSİZ - KONTROL ET"
            inferred_cat = ""
            inferred_sub_cat = ""
            
            word = ext_name.split()[0] if " " in ext_name else ext_name
            infer_matches = df_main[df_main['label'].str.contains(word, case=False, na=False, regex=False)]
            
            if not infer_matches.empty:
                try:
                    top_matches = infer_matches['mainCategory'].value_counts()
                    valid_cats = top_matches[top_matches.index != ""]
                    if not valid_cats.empty:
                        best_cat_name = valid_cats.index[0]
                        sample_row = infer_matches[infer_matches['mainCategory'] == best_cat_name].iloc[0]
                        inferred_main_cat = sample_row['mainCategory']
                        inferred_cat = sample_row['category'] if pd.notna(sample_row['category']) else ""
                        inferred_sub_cat = sample_row['subCategory'] if pd.notna(sample_row['subCategory']) else ""
                except:
                    pass

            new_rows.append({
                'label': ext_name,
                'price1': final_price,
                'currencyAbbr': item['currency'],
                'mainCategory': inferred_main_cat,
                'category': inferred_cat,
                'subCategory': inferred_sub_cat,
                'status': 1
            })
            unmatched_items.append({"name": ext_name, "price": final_price, "currency": item['currency'], "source": "Chat-Image"})

if new_rows:
    df_main = pd.concat([df_main, pd.DataFrame(new_rows)], ignore_index=True)

df_main.to_excel(OUTPUT_EXCEL, index=False)

print(f"Eşleşen (Birebir): {matched_count}")
print(f"Çoklu Güncellenen (Multi): {multi_matched_count}")
print(f"Yeni Olarak Eklenen: {len(new_rows)}")
print(f"Fiyat Düşüş Korumasıyla Reddedilen: {len(price_drop_warnings)}")

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Sohbet Üzerinden Görsel Okumaları - İlk 4'lü)\n")
    f.write(f"- 4 Görsel saniyeler içinde okundu toplam **{len(batch_1_items)}** ürün çıkarıldı.\n")
    f.write(f"- Tam eşleşip güncellenen: **{matched_count}**, Multi-Varyasyon Değişen: **{multi_matched_count}**.\n")
    f.write(f"- Altyapıda bulunamayan **{len(new_rows)}** ürün kategori Inference metoduyla veritabanına eklendi!\n")
    f.write(f"- Güvenlik nedeniyle düşük teklif veren (**{len(price_drop_warnings)}**) satır ezilmekten KORUNDU.\n")
    for w in price_drop_warnings:
        f.write(f"  {w}\n")

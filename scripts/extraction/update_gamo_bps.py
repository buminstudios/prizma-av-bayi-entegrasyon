import pandas as pd
from thefuzz import process, fuzz
import re

FILE_PATH = 'prizma-urunler-guncel.xlsx'

gamo_items = [
    {"name": "GAMO PT-85 BLOWBACK 4,5 MM HAVALI TABANCA", "price": 5950, "currency": "TL"},
    {"name": "GAMO C-15 BLOWBACK 4,5 MM HAVALI TABANCA", "price": 5700, "currency": "TL"},
    {"name": "GAMO GAZ TÜPÜ 12 GR", "price": 22.25, "currency": "TL"},
    {"name": "GAMO HAVALI SAÇMA MAGNUM TEN.250'Lİ 5,5 MM", "price": 5.20, "currency": "EUR"},
    {"name": "GAMO HAVALI SAÇMA HUNTER 5,5 MM 250Lİ", "price": 5.20, "currency": "EUR"},
    {"name": "GAMO HAVALI SAÇMA TS-22 TEN. 5,5 MM", "price": 5.80, "currency": "EUR"},
    {"name": "GAMO HAVALI SAÇMA 10X HOLLOW POINT 5,5 MM", "price": 5.20, "currency": "EUR"}
]

bps_raw = [
    {"kalibre": "12", "gram": "22", "tapa": "POWER", "sacma_no": "BILDIRCIN", "price_1000": 18000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "24", "tapa": "POWER&SKEET", "sacma_no": "EXTRA TRAP&SKEET", "price_1000": 18000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "28", "tapa": "POWER/BIOR", "sacma_no": "7-10", "price_1000": 20500, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "30", "tapa": "POWER/BIOR", "sacma_no": "3-10", "price_1000": 20600, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "28/30", "tapa": "KEÇE", "sacma_no": "5-10", "price_1000": 22600, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "32", "tapa": "POWER", "sacma_no": "1-11", "price_1000": 21200, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "32", "tapa": "KEÇE", "sacma_no": "5-9", "price_1000": 23000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "32", "tapa": "DİSPERSANTE", "sacma_no": "8-9", "price_1000": 23000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "33", "tapa": "BIOR", "sacma_no": "3-11", "price_1000": 21400, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "34", "tapa": "POWER", "sacma_no": "1-11", "price_1000": 21400, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "34", "tapa": "KEÇE", "sacma_no": "5-9", "price_1000": 24000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "36", "tapa": "POWER", "sacma_no": "1-7", "price_1000": 23000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "40", "tapa": "POWER", "sacma_no": "1-5", "price_1000": 25000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "50", "tapa": "POWER", "sacma_no": "1-5", "price_1000": 30000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "", "tapa": "POWER", "sacma_no": "EXTRA SESLİ FİŞEK", "price_1000": 18000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "28", "tapa": "", "sacma_no": "SLUG (YİVLİ)", "price_1000": 31000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "29", "tapa": "", "sacma_no": "SLUG (EXTRA GUALANDI)", "price_1000": 35000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "29", "tapa": "", "sacma_no": "RED STAR SLUG", "price_1000": 38000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "25.5", "tapa": "", "sacma_no": "SABOT SLUG", "price_1000": 56000, "ambalaj_kutu": 5},
    {"kalibre": "12", "gram": "34", "tapa": "", "sacma_no": "BİLYA TEK KURŞUN", "price_1000": 32000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "37", "tapa": "", "sacma_no": "7/0 (27 ADET) ŞEVROTİN", "price_1000": 29000, "ambalaj_kutu": 10},
    {"kalibre": "12", "gram": "34", "tapa": "", "sacma_no": "11/0 (3X3) ŞEVROTİN", "price_1000": 27000, "ambalaj_kutu": 10},
    
    {"kalibre": "16", "gram": "28", "tapa": "POWER", "sacma_no": "1-3-5-7-9", "price_1000": 20000, "ambalaj_kutu": 25},
    {"kalibre": "16", "gram": "", "tapa": "", "sacma_no": "SLUG", "price_1000": 31000, "ambalaj_kutu": 25},
    {"kalibre": "16", "gram": "", "tapa": "", "sacma_no": "ŞEVROTİN (3X3)", "price_1000": 27000, "ambalaj_kutu": 25},

    {"kalibre": "20", "gram": "22", "tapa": "POWER", "sacma_no": "9-10", "price_1000": 20400, "ambalaj_kutu": 25},
    {"kalibre": "20", "gram": "28", "tapa": "POWER/BIOR", "sacma_no": "5-10", "price_1000": 20800, "ambalaj_kutu": 25},
    {"kalibre": "20", "gram": "28", "tapa": "POWER", "sacma_no": "4-10", "price_1000": 21600, "ambalaj_kutu": 25},
    {"kalibre": "20", "gram": "", "tapa": "", "sacma_no": "ŞEVROTİN (3X3)", "price_1000": 25000, "ambalaj_kutu": 25},
    {"kalibre": "20", "gram": "", "tapa": "", "sacma_no": "SLUG", "price_1000": 31000, "ambalaj_kutu": 25},

    {"kalibre": "28", "gram": "24", "tapa": "POWER", "sacma_no": "4-10", "price_1000": 22000, "ambalaj_kutu": 25},
    {"kalibre": "28", "gram": "15", "tapa": "", "sacma_no": "SLUG", "price_1000": 31000, "ambalaj_kutu": 25},

    {"kalibre": "36", "gram": "12", "tapa": "POWER", "sacma_no": "4-10", "price_1000": 21000, "ambalaj_kutu": 25},
    {"kalibre": "36", "gram": "7.5", "tapa": "", "sacma_no": "SLUG", "price_1000": 31000, "ambalaj_kutu": 25},

    {"kalibre": "12", "gram": "34", "tapa": "POWER", "sacma_no": "SÜRSARJLI FİŞEK", "price_1000": 24000, "ambalaj_kutu": 25},
    {"kalibre": "12", "gram": "", "tapa": "BIOR", "sacma_no": "RUBBER FİŞEK", "price_1000": 24000, "ambalaj_kutu": 10},
]

# Build BPS items for uniform processing
bps_items = []
for b in bps_raw:
    parts = ["BPS"]
    if b["kalibre"]:
        parts.append(f"{b['kalibre']} CAL")
    if b["gram"]:
        parts.append(f"{b['gram']} GR")
    if b["tapa"]:
        parts.append(b["tapa"])
    if b["sacma_no"]:
        parts.append(b["sacma_no"])
    
    parts.append("AV FİŞEĞİ") # Common suffix for DB search
    
    full_name = " ".join(parts)
    toptan_kutu = (b["price_1000"] / 1000.0) * b["ambalaj_kutu"]
    
    bps_items.append({
        "name": full_name,
        "price": toptan_kutu,
        "currency": "TL",
        "brand": "BPS"
    })

# Add GAMO items
all_items = bps_items.copy()
for g in gamo_items:
    g['brand'] = 'GAMO'
    all_items.append(g)

def clean_name(n):
    n = str(n).upper()
    n = re.sub(r'AV FİŞEĞİ|12 CAL\.|12 CAL|20 CAL\.|20 CAL|36 CAL\.|36 CAL|FİŞEK|GR\.|GR|,|:', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

df_main = pd.read_excel(FILE_PATH)
existing_series = df_main['label'].dropna()
existing_names = existing_series.tolist()
db_map = {clean_name(name): name for name in existing_names if 'BPS' in str(name).upper() or 'GAMO' in str(name).upper()}

matched_count = 0
new_rows = []

for item in all_items:
    ext_name_clean = clean_name(item['name'])
    # logic: perakende = (toptan * 1.35) / 1.20
    final_price = round((item['price'] * 1.35) / 1.20, 2)
    
    match_result = process.extractOne(ext_name_clean, list(db_map.keys()), scorer=fuzz.token_set_ratio)
    
    if match_result and match_result[1] >= 85:
        best_clean = match_result[0]
        original_db_name = db_map[best_clean]
        
        df_main.loc[df_main['label'] == original_db_name, 'price1'] = final_price
        df_main.loc[df_main['label'] == original_db_name, 'currencyAbbr'] = item['currency']
        df_main.loc[df_main['label'] == original_db_name, 'brand'] = item['brand']
        matched_count += 1
        print(f"[{item['brand']}] Güncellendi: '{item['name']}' -> DB Yeri: '{original_db_name}' (Skor: {match_result[1]}, Yeni Fiyat: {final_price} {item['currency']})")
    else:
        # Determine categories
        if item['brand'] == 'BPS':
            main_cat = "AV FİŞEKLERİ"
            cat = "Yerli Fişekler"
        else:
            if "TABANCA" in item['name']:
                main_cat = "Atıcılık & Airsoft"
                cat = "Havalı"
            elif "SAÇMA" in item['name']:
                main_cat = "Atıcılık & Airsoft"
                cat = "Havalı Mühimmatı"
            else:
                main_cat = "Atıcılık & Airsoft"
                cat = "Aksesuarlar"

        new_rows.append({
            'label': item['name'],
            'price1': final_price,
            'currencyAbbr': item['currency'],
            'status': 1,
            'brand': item['brand'],
            'mainCategory': main_cat,
            'category': cat,
            'subCategory': ""
        })
        print(f"[{item['brand']}] YENİ EKLENDİ: '{item['name']}' (Fiyat: {final_price} {item['currency']}) (En iyi eşleşme: {match_result[0] if match_result else 'Yok'} skor {match_result[1] if match_result else 0})")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

df_main.to_excel(FILE_PATH, index=False)
print(f"\nİşlem Tamam. Toplam Güncellenen: {matched_count}, Toplam Eklenen: {len(new_rows)}")

import pandas as pd
from thefuzz import process, fuzz
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

rc_items = [
    {"name": "RC 2 COMP.LINE 28 GR FİŞEK", "price": 23.150, "box": 25},
    {"name": "RC 30 CACCIA 30 GR FİŞEK", "price": 25.150, "box": 25},
    {"name": "RC 31 TITANO GR FİŞEK", "price": 25.425, "box": 25},
    {"name": "RC 32 CACCIA 32 GR FİŞEK", "price": 26.250, "box": 25},
    {"name": "RC 1 CACCIA 33 GR FİŞEK", "price": 26.500, "box": 25},
    {"name": "RC SIPE 32 GR FİŞEK", "price": 34.600, "box": 25},
    {"name": "RC S4 SPECIAL 33 GR FİŞEK", "price": 34.900, "box": 25},
    {"name": "RC 2 CACCIA 34 GR FİŞEK", "price": 27.500, "box": 25},
    {"name": "RC 2 KAĞIT KOVAN KEÇE TAPA 32 GR FİŞEK", "price": 33.800, "box": 25},
    {"name": "RC 20 KAL SİPE FİŞEK 25 GR", "price": 28.400, "box": 25},
    {"name": "RC 20 SİPE KEÇE TAPA 26 GR FİŞEK", "price": 29.000, "box": 25},
    {"name": "RC 20 T3 28 GR FİŞEK", "price": 27.500, "box": 25},
    {"name": "RC CAMOUFLAGE 34 GR FİŞEK", "price": 31.350, "box": 25},
    {"name": "RC 1 GAME LINE 36 GR FİŞEK", "price": 31.350, "box": 25},
    {"name": "RC 3 DİSPERSANTE 33 GR FİŞEK", "price": 30.150, "box": 25},
    {"name": "RC 4 DİSPERSANTE 34 GR FİŞEK", "price": 33.280, "box": 25},
    {"name": "RC 2 COMP.LINE TRAP 24 GR FİŞEK", "price": 22.280, "box": 25},
    {"name": "RC 2 SKEET 24 GR FİŞEK", "price": 23.000, "box": 25},
    {"name": "RC 4 HYPERFAST 24 GR TRAP FİŞEK", "price": 29.325, "box": 25},
    {"name": "RC 4 CHAMPION EXCELLENCE 24 GR TRAP FİŞEK", "price": 29.225, "box": 25},
    {"name": "RC RED SHOT SUP.NIK 24 GR FİŞEK", "price": 29.750, "box": 25},
    {"name": "RC 4 ŞEVROTTİN FİŞEK", "price": 52.750, "box": 10},
    {"name": "RC TEK KURŞUN 32 GR FİŞEK", "price": 67.500, "box": 10},
]

df_main = pd.read_excel(FILE_PATH)
existing_names = df_main['label'].dropna().astype(str).tolist()

matched_count = 0
multi_matched_count = 0
new_rows = []

for item in rc_items:
    ext_name = item['name']
    
    # Calculate price based on standard formula -> Final Price = (base_price * box_count * 1.35) / 1.20
    final_price = round((item['price'] * item['box'] * 1.35) / 1.20, 2)

    match_result = process.extractOne(ext_name, existing_names, scorer=fuzz.token_sort_ratio)
    
    if match_result and match_result[1] >= 85:
        best_match_name = match_result[0]
        df_main.loc[df_main['label'] == best_match_name, 'price1'] = final_price
        df_main.loc[df_main['label'] == best_match_name, 'currencyAbbr'] = 'TL'
        df_main.loc[df_main['label'] == best_match_name, 'brand'] = 'RC'
        matched_count += 1
    else:
        set_matches = process.extract(ext_name, existing_names, limit=20, scorer=fuzz.token_set_ratio)
        valid_set_matches = [m for m in set_matches if m[1] >= 90 and 'RC ' in m[0].upper()]
        
        if valid_set_matches:
            for m in valid_set_matches:
                db_name = m[0]
                df_main.loc[df_main['label'] == db_name, 'price1'] = final_price
                df_main.loc[df_main['label'] == db_name, 'currencyAbbr'] = 'TL'
                df_main.loc[df_main['label'] == db_name, 'brand'] = 'RC'
                multi_matched_count += 1
        else:
            inferred_main_cat = "AV FİŞEKLERİ"
            new_rows.append({
                'label': ext_name,
                'price1': final_price,
                'currencyAbbr': 'TL',
                'status': 1,
                'brand': 'RC',
                'mainCategory': inferred_main_cat,
                'category': "RC Fişekler",
                'subCategory': ""
            })

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

df_main.to_excel(FILE_PATH, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (RC Fişek Görsel Fiyatları)\n")
    f.write(f"- Yüklenen görseldeki RC marka fişek fiyatları (adet bazlı toptan) işlendi.\n")
    f.write(f"- Formül: (Toptan * Kutu * 1.35) / 1.20 kullanıldı. Saçmalar 25, Şevrotin/Kurşun 10 kutu adetiyle çarpıldı.\n")
    f.write(f"- Birebir Eşleşen: {matched_count}, Multi/Varyasyon Dağıtılan: {multi_matched_count}, Yeni Eklenen: {len(new_rows)}\n")

print(f"Toplam Birebir: {matched_count}")
print(f"Toplam Dağıtılan (Multi): {multi_matched_count}")
print(f"Sisteme Yeni Eklenen: {len(new_rows)}")
print("İşlem Tamamlandı.")

import os
import pandas as pd
from thefuzz import process, fuzz
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASG_FILE = os.path.join(BASE_DIR, 'ürünler fiyatlar/ASG FİYAT LİSTESİ 26.12.2025.xlsx')
ORIGINAL_EXCEL = os.path.join(BASE_DIR, 'prizma-urunler-guncel.xlsx')
OUTPUT_EXCEL = os.path.join(BASE_DIR, 'prizma-urunler-guncel.xlsx')
ALIAS_CSV = os.path.join(BASE_DIR, 'alias_dict.csv')

def clean_price(price_str):
    if pd.isna(price_str):
        return None
    s = str(price_str).replace('₺', '').replace('TL', '').replace('$', '').replace('€', '').strip()
    if ',' in s and '.' in s:
        if s.rfind(',') > s.rfind('.'):
            s = s.replace('.', '').replace(',', '.')
        else:
            s = s.replace(',', '')
    elif ',' in s:
        s = s.replace(',', '.')
    try:
        return float(s)
    except:
        return None

alias_dict = {}
if os.path.exists(ALIAS_CSV):
    try:
        df_alias = pd.read_csv(ALIAS_CSV)
        for _, row in df_alias.iterrows():
            if pd.notna(row.get('Okunan_Isim_Toptanci')) and pd.notna(row.get('Asil_Ideasoft_Ismi_SECILEN')):
                t_name = str(row['Okunan_Isim_Toptanci']).strip()
                i_name = str(row['Asil_Ideasoft_Ismi_SECILEN']).strip()
                if i_name:
                    alias_dict[t_name] = i_name
    except:
        pass

df_asg = pd.read_excel(ASG_FILE)
extracted_items = []
n_col_idx = -1
p_col_idx = -1

for row_idx, row in df_asg.iterrows():
    # Detect header row dynamically
    if n_col_idx == -1 or p_col_idx == -1:
        for idx, val in enumerate(row.values):
            s = str(val).upper()
            if 'ADI' in s and n_col_idx == -1:
                n_col_idx = idx
            if ('PERAKENDE' in s or 'PAREKENDE' in s) and p_col_idx == -1:
                p_col_idx = idx
        continue # Found header or still looking

    # Read records
    if n_col_idx != -1 and p_col_idx != -1:
        item_name = row.iloc[n_col_idx]
        item_price_str = row.iloc[p_col_idx]
        
        # skip sub-headers like "HAVALI TABANCA" where price is NaN
        if pd.notna(item_name) and pd.notna(item_price_str) and str(item_name).strip().upper() != 'ADI':
            price_f = clean_price(item_price_str)
            if price_f and price_f > 0:
                kdv_haric = price_f / 1.20
                clean_name = str(item_name).replace('\n', ' ').strip()
                match_name = "ASG " + clean_name.replace('"', ' İnc').replace('2,5', '2.5').replace('Revolver', 'Toplu')
                
                extracted_items.append({
                    "name": clean_name, 
                    "match_name": match_name,
                    "price": round(kdv_haric, 2), 
                    "currency": "EUR", 
                    "source": "ASG (Excel)"
                })

print(f"Çıkarılan ASG ürün adedi: {len(extracted_items)}")
for i in extracted_items[:5]:
    print("-", i)

df_main = pd.read_excel(ORIGINAL_EXCEL)
existing_names = df_main['label'].dropna().astype(str).tolist()

matched_count = 0
multi_matched_count = 0
new_rows = []

for item in extracted_items:
    ext_name = item['name']
    match_name = item['match_name']
    
    if ext_name in alias_dict:
        db_match_name = alias_dict[ext_name]
        df_main.loc[df_main['label'] == db_match_name, 'price1'] = item['price']
        df_main.loc[df_main['label'] == db_match_name, 'currencyAbbr'] = item['currency']
        matched_count += 1
        continue

    # Use match_name for matching logic to increase score
    match_result = process.extractOne(match_name, existing_names, scorer=fuzz.token_sort_ratio)
    
    if match_result and match_result[1] >= 85:
        best_match_name = match_result[0]
        df_main.loc[df_main['label'] == best_match_name, 'price1'] = item['price']
        df_main.loc[df_main['label'] == best_match_name, 'currencyAbbr'] = item['currency']
        matched_count += 1
    else:
        set_matches = process.extract(match_name, existing_names, limit=20, scorer=fuzz.token_set_ratio)
        valid_set_matches = [m for m in set_matches if m[1] >= 90]
        
        if valid_set_matches and len(ext_name) >= 5:
            for m in valid_set_matches:
                db_name = m[0]
                df_main.loc[df_main['label'] == db_name, 'price1'] = item['price']
                df_main.loc[df_main['label'] == db_name, 'currencyAbbr'] = item['currency']
                multi_matched_count += 1
        else:
            inferred_main_cat = "KATEGORİSİZ - KONTROL ET"
            word = ext_name.split()[0] if " " in ext_name else ext_name
            infer_matches = df_main[df_main['label'].str.contains(word, case=False, na=False, regex=False)]
            if not infer_matches.empty:
                inferred_main_cat = infer_matches.iloc[0].get('mainCategory', inferred_main_cat)

            new_rows.append({
                'label': ext_name, 
                'price1': item['price'], 
                'currencyAbbr': item['currency'], 
                'status': 1,
                'mainCategory': inferred_main_cat,
                'category': "",
                'subCategory': ""
            })

print(f"Eşleşen (Birebir): {matched_count}")
print(f"Eşleşen (Multi/Varyasyon): {multi_matched_count}")
print(f"Yeni Olarak Eklenen: {len(new_rows)}")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

df_main.to_excel(OUTPUT_EXCEL, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (ASG Fiyat Listesi Eklendi)\n")
    f.write(f"- Ürünler ve fiyatlar klasöründeki ASG Fiyat listesinden ürünler işlendi.\n")
    f.write(f"- Perakende fiyat üzerinden KDV hariç euro fiyatlar girildi.\n")
    f.write(f"- Birebir Eşleşen: {matched_count}, Multi/Varyasyon: {multi_matched_count}, Eklenen: {len(new_rows)}\n")

print("ASG İşlemi Tamamlandı.")

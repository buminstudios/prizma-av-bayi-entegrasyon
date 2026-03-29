import os
import pandas as pd
import pdfplumber
import re
from thefuzz import process, fuzz
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICELISTS_DIR = os.path.join(BASE_DIR, 'yeni ürünler ')
ORIGINAL_EXCEL = os.path.join(BASE_DIR, 'prizma-urunler-guncel.xlsx')
OUTPUT_EXCEL = os.path.join(BASE_DIR, 'prizma-urunler-guncel.xlsx')
UNMATCHED_CSV = os.path.join(BASE_DIR, 'eslesmeyenler.csv')
ALIAS_CSV = os.path.join(BASE_DIR, 'alias_dict.csv')
REVIEW_CSV = os.path.join(BASE_DIR, 'onay_bekleyen_eslesmeler.csv')

def get_currency(price_str):
    s = str(price_str).upper()
    if '$' in s or 'USD' in s: return 'USD'
    if '€' in s or 'EUR' in s: return 'EUR'
    return 'TL'

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

# Load Alias Dict
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
        print(f"Alias sözlüğünden {len(alias_dict)} özel eşleşme yüklendi.")
    except Exception as e:
        print(f"Alias sözlüğü yükleme hatası: {e}")

extracted_items_dict = {}

ekol_products = {
    "Ekol ES 55": 2400.00, "Ekol ES 66": 3120.00, "Ekol ES 66 C": 3120.00, "Ekol ES P66": 2700.00,
    "Ekol ES P66 C": 2580.00, "Ekol ES P92": 3060.00, "Ekol ES P92 B": 3840.00, "Ekol ES P95 B": 4560.00,
    "Ekol ES 1911": 3840.00, "Ekol ES 1911 C": 3840.00, "Ekol FOWLER": 2160.00, "Ekol HAVALI TÜFEK MAJÖR": 3300.00,
    "Ekol ULTIMATE": 3300.00, "Ekol THUNDER": 3480.00, "Ekol THUNDER-M": 3600.00, "Ekol ULTIMATE-F": 3720.00,
    "Ekol MAJÖR-F": 3720.00, "Ekol THUNDER-F": 3960.00, "Ekol THUNDER-FM": 4080.00, "Ekol AK": 4200.00,
    "Ekol AKL": 4200.00, "Ekol M": 4080.00, "Ekol ML": 4080.00, "Ekol MS": 4080.00, "Ekol MC": 4080.00,
    "Ekol PCP 1": 10200.00, "Ekol PCP 2": 10200.00, "Ekol PCP 3": 10200.00, "Ekol PCP 4": 10200.00,
    "Ekol ALP": 2916.00, "Ekol ALP-2": 2916.00, "Ekol ALPER": 2916.00, "Ekol ARAS MAGNUM": 3240.00,
    "Ekol ARAS COMPACT": 3240.00, "Ekol BOTAN": 2268.00, "Ekol DİCLE": 3240.00, "Ekol FIRAT COMPACT": 3240.00,
    "Ekol FIRAT MAGNUM": 3240.00, "Ekol FIRAT P92": 3240.00, "Ekol FIRAT PA92": 3240.00, "Ekol FIRAT PB92": 3240.00,
    "Ekol FIRAT PC92": 3240.00, "Ekol GEDİZ": 3412.80, "Ekol KURA": 2376.00, "Ekol LADY": 2433.60,
    "Ekol MAJAROV": 2678.40, "Ekol KURUSIKI MAJÖR": 2433.60, "Ekol NİG 211": 3456.00, "Ekol P29": 2736.00,
    "Ekol P29 REV 2": 2916.00, "Ekol SAVA": 3024.00, "Ekol SPECIAL 99": 2736.00, "Ekol SPECIAL 99 REV 2": 2916.00,
    "Ekol TİSA": 2160.00, "Ekol TUNA": 1944.00, "Ekol VOLGA": 2088.00, "Ekol ARDA": 2592.00,
    "Ekol VIPER LITE": 3096.00, "Ekol VIPER 2,5": 3168.00, "Ekol VIPER 3": 3168.00, "Ekol VIPER 4,5": 3240.00,
    "Ekol VIPER 6": 3312.00
}

for ext_name, original_price in ekol_products.items():
    zamli_fiyat = original_price * 1.35
    kdv_haric_fiyat = zamli_fiyat / 1.20
    extracted_items_dict[ext_name] = {
        "name": ext_name, "price": round(kdv_haric_fiyat, 2), "currency": "TL", "source": "Image-Ekol"
    }

print("Adım 1: Tedarikçi PDF ve Excel'leri okuma işlemi...")
files = [f for f in os.listdir(PRICELISTS_DIR) if not f.startswith('.')]

for filename in files:
    filepath = os.path.join(PRICELISTS_DIR, filename)
    name_col_idx = -1
    price_col_idx = -1
    has_perakende_header = False
    
    if filename.endswith('.pdf'):
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    for table in tables:
                        is_header = False
                        tmp_name_idx = -1
                        tmp_price_idx = -1
                        tmp_has_perakende = False
                        
                        for row_idx, row in enumerate(table):
                            if not row: continue
                            for c_idx, cell in enumerate(row):
                                if not cell: continue
                                c_str = str(cell).upper()
                                if 'ÜRÜN' in c_str or 'AÇIKLAMA' in c_str or 'MODEL' in c_str:
                                    tmp_name_idx = c_idx
                                    is_header = True
                                if 'PERAKENDE' in c_str or 'PAREKENDE' in c_str or 'PARAKENDE' in c_str:
                                    tmp_price_idx = c_idx
                                    tmp_has_perakende = True
                                    is_header = True
                                elif ('FİYAT' in c_str or 'TOPTAN' in c_str or 'TL' in c_str) and tmp_price_idx == -1:
                                    tmp_price_idx = c_idx
                                    is_header = True
                                
                            if tmp_name_idx != -1 and tmp_price_idx != -1:
                                name_col_idx = tmp_name_idx
                                price_col_idx = tmp_price_idx
                                has_perakende_header = tmp_has_perakende
                                break
                                
                        if name_col_idx != -1 and price_col_idx != -1:
                            for row in table[row_idx+1:]:
                                if len(row) > max(name_col_idx, price_col_idx):
                                    item_name = row[name_col_idx]
                                    item_price_str = row[price_col_idx]
                                    if item_name and item_price_str and 'TOPTAN' not in str(item_name).upper():
                                        currency = get_currency(item_price_str)
                                        price_f = clean_price(item_price_str)
                                        if price_f and price_f > 0:
                                            if has_perakende_header:
                                                kdv_haric = price_f / 1.20
                                            else:
                                                kdv_haric = (price_f * 1.35) / 1.20
                                            clean_name = str(item_name).replace('\n', ' ').strip()
                                            extracted_items_dict[clean_name] = {"name": clean_name, "price": round(kdv_haric, 2), "currency": currency, "source": f"{filename} (PDF)"}
        except Exception as e:
            print(f"HATA PDF ({filename}): {e}")

    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        try:
            dfs_sup = pd.read_excel(filepath, sheet_name=None)
            for sheet_name, df_sup in dfs_sup.items():
                n_col = None
                p_col = None
                has_perakende_eval = False
                for c in df_sup.columns:
                    c_str = str(c).upper()
                    if 'ÜRÜN' in c_str or 'AÇIKLAMA' in c_str or 'MODEL' in c_str or 'AD' in c_str:
                        if n_col is None: n_col = c
                    if 'PERAKENDE' in c_str or 'PAREKENDE' in c_str or 'PARAKENDE' in c_str:
                        p_col = c
                        has_perakende_eval = True
                    elif ('FİYAT' in c_str or 'TOPTAN' in c_str or 'FİYATI' in c_str) and p_col is None:
                        p_col = c
                
                if n_col is not None and p_col is not None:
                    for _, row in df_sup.iterrows():
                        item_name = row[n_col]
                        item_price_str = row[p_col]
                        if pd.notna(item_name) and pd.notna(item_price_str):
                            currency = get_currency(item_price_str)
                            price_f = clean_price(item_price_str)
                            if price_f and price_f > 0:
                                if has_perakende_eval:
                                    kdv_haric = price_f / 1.20
                                else:
                                    kdv_haric = (price_f * 1.35) / 1.20
                                clean_name = str(item_name).replace('\n', ' ').strip()
                                extracted_items_dict[clean_name] = {"name": clean_name, "price": round(kdv_haric, 2), "currency": currency, "source": f"{filename} - Tab:{sheet_name}"}
        except Exception as e:
            print(f"HATA EXCEL ({filename}): {e}")

extracted_items = list(extracted_items_dict.values())
print(f"Toplam çıkarılan unique ürün adedi: {len(extracted_items)}")

print("Adım 2: Orijinal İdeasoft Excel verisi okunuyor...")
df_main = pd.read_excel(ORIGINAL_EXCEL)
existing_names = df_main['label'].dropna().astype(str).tolist()

matched_count = 0
unmatched_items = []
multi_matched_count = 0
new_rows = []
price_drop_warnings = []

print("Adım 3: Faz 5 Çoklu Eşleştirme (Multi-Update & Inference) Çalışıyor...")

for item in extracted_items:
    ext_name = item['name']
    
    # 1. Alias (Öğrenilmiş Eşleşme) Kontrolü
    if ext_name in alias_dict:
        db_match_name = alias_dict[ext_name]
        try:
            current_price_raw = df_main.loc[df_main['label'] == db_match_name, 'price1'].values[0]
            current_price = float(str(current_price_raw).replace(',', '.'))
        except:
            current_price = 0.0

        if current_price > 0 and item['price'] < current_price:
            price_drop_warnings.append(f"- **DÜŞÜK FİYAT ENGELLENDİ**: '{ext_name}' (Alias: {db_match_name}) Mevcut: {current_price}, Yeni: {item['price']}.")
        else:
            df_main.loc[df_main['label'] == db_match_name, 'price1'] = item['price']
            df_main.loc[df_main['label'] == db_match_name, 'currencyAbbr'] = item['currency']
            matched_count += 1
        continue

    # 2. Bulanık Arama (Sort Testi)
    match_result = process.extractOne(ext_name, existing_names, scorer=fuzz.token_sort_ratio)
    
    if match_result and match_result[1] >= 85:
        # Birebir Net Eşleşme
        best_match_name = match_result[0]
        try:
            current_price_raw = df_main.loc[df_main['label'] == best_match_name, 'price1'].values[0]
            current_price = float(str(current_price_raw).replace(',', '.'))
        except:
            current_price = 0.0

        if current_price > 0 and item['price'] < current_price:
            price_drop_warnings.append(f"- **DÜŞÜK FİYAT ENGELLENDİ**: '{ext_name}' (Mevcut: {current_price}, Yeni: {item['price']}).")
        else:
            df_main.loc[df_main['label'] == best_match_name, 'price1'] = item['price']
            df_main.loc[df_main['label'] == best_match_name, 'currencyAbbr'] = item['currency']
            matched_count += 1
    
    else:
        # 3. Yarı-Eşleşme Testi (Set Ratio)
        set_matches = process.extract(ext_name, existing_names, limit=20, scorer=fuzz.token_set_ratio)
        valid_set_matches = [m for m in set_matches if m[1] >= 90]
        
        if valid_set_matches and len(ext_name) >= 5:
            # Multi-Update -> BULUNAN TÜM NET VARYASYONLARA FİYATI DAĞIT!
            for m in valid_set_matches:
                db_name = m[0]
                try:
                    current_price_raw = df_main.loc[df_main['label'] == db_name, 'price1'].values[0]
                    current_price = float(str(current_price_raw).replace(',', '.'))
                except:
                    current_price = 0.0

                if current_price > 0 and item['price'] < current_price:
                    price_drop_warnings.append(f"- **DÜŞÜK FİYAT ENGELLENDİ (MULTI-UPDATE)**: '{ext_name}' (İdeasoft: {db_name}) Mevcut: {current_price}, Yeni: {item['price']}.")
                else:
                    df_main.loc[df_main['label'] == db_name, 'price1'] = item['price']
                    df_main.loc[df_main['label'] == db_name, 'currencyAbbr'] = item['currency']
                    multi_matched_count += 1
        else:
            # 4. Hiçbir yere uymuyor. Yepyeni Parça -> Kategori Çalma (Category Inference)
            inferred_main_cat = "KATEGORİSİZ - KONTROL ET"
            inferred_cat = ""
            inferred_sub_cat = ""
            
            # Find the closest category by partial name lookup
            word = ext_name.split()[0] if " " in ext_name else ext_name
            infer_matches = df_main[df_main['label'].str.contains(word, case=False, na=False, regex=False)]
            
            if not infer_matches.empty:
                # En çok satan veya en ilk bulunan benzer ismin kategorisini çal!
                row_copy = infer_matches.iloc[0]
                inferred_main_cat = row_copy.get('mainCategory', inferred_main_cat)
                inferred_cat = row_copy.get('category', "")
                inferred_sub_cat = row_copy.get('subCategory', "")

            unmatched_items.append(item)
            new_rows.append({
                'label': ext_name, 
                'price1': item['price'], 
                'currencyAbbr': item['currency'], 
                'status': 1,
                'mainCategory': inferred_main_cat,
                'category': inferred_cat,
                'subCategory': inferred_sub_cat
            })

print(f"Eşleşen ve Güncellenen: {matched_count}")
print(f"Varyasyonlara Dağıtılan (Multi-Update): {multi_matched_count}")
print(f"Yepyeni Olarak Eklenen: {len(new_rows)}")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

print("Adım 4: Dosyalar kaydediliyor...")
try:
    df_main.to_excel(OUTPUT_EXCEL, index=False)
except Exception as e:
    print(f"Excel kaydetme hatası: {e}")

if unmatched_items:
    pd.DataFrame(unmatched_items).to_csv(UNMATCHED_CSV, index=False, encoding='utf-8')

# Devlog
try:
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (FAZ 5: Çoklu Güncelleme / Multi-Update)\n")
        f.write(f"- Faz 4'teki onay sistemi iptal edilip, toptancı fiyatının İdeasoft tarafındaki **tüm renk/kapsayıcı varyasyonlara** dağıtılması kuralı eklendi.\n")
        f.write(f"- Toplam **{multi_matched_count}** adet varyasyon otomatik tespit edilerek baz fiyatlarıyla ezildi.\n")
        f.write(f"- Sistemde tamamen yepyeni tespit edilen **{len(new_rows)}** ürünün İdeasoft kategorileri 'Benzerinden Kopyala (Inference)' yöntemiyle atanarak En Alta eklendi!\n")
except Exception as e:
    pass

print("FAZ 4 İŞLEM TAMAMLANDI")

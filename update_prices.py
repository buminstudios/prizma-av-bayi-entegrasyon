import os
import pandas as pd
import pdfplumber
import re
from thefuzz import process, fuzz
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRICELISTS_DIR = os.path.join(BASE_DIR, 'ürünler fiyatlar')
ORIGINAL_EXCEL = os.path.join(BASE_DIR, 'prizma-urunler.xlsx')
OUTPUT_EXCEL = os.path.join(BASE_DIR, 'prizma-urunler-guncel.xlsx')
UNMATCHED_CSV = os.path.join(BASE_DIR, 'eslesmeyenler.csv')

def get_currency(price_str):
    s = str(price_str).upper()
    if '$' in s or 'USD' in s: return 'USD'
    if '€' in s or 'EUR' in s: return 'EUR'
    return 'TL'

def clean_price(price_str):
    if not isinstance(price_str, str):
        return price_str
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

# Dictionary to hold the extracted items
# We'll use a dict with Extracted Name -> {"name": "", "price": float, "currency": "TL", "source": ""}
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

# Add Ekol products manually
for ext_name, original_price in ekol_products.items():
    zamli_fiyat = original_price * 1.35
    kdv_haric_fiyat = zamli_fiyat / 1.20
    extracted_items_dict[ext_name] = {
        "name": ext_name, "price": round(kdv_haric_fiyat, 2), "currency": "TL", "source": "Image-Ekol"
    }

print("Adım 1: Tedarikçi PDF ve Excel'leri işleniyor (Multi-sheet & Toptan/Perakende Zekası devrede)...")
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
                        # Find headers
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
                                    # Fallback price column, wait maybe there's a real perakende later in row
                                    tmp_price_idx = c_idx
                                    is_header = True
                                
                            if tmp_name_idx != -1 and tmp_price_idx != -1:
                                name_col_idx = tmp_name_idx
                                price_col_idx = tmp_price_idx
                                has_perakende_header = tmp_has_perakende
                                break # headers found
                                
                        if name_col_idx != -1 and price_col_idx != -1:
                            for row in table[row_idx+1:]:
                                if len(row) > max(name_col_idx, price_col_idx):
                                    item_name = row[name_col_idx]
                                    item_price_str = row[price_col_idx]
                                    
                                    if item_name and item_price_str and 'TOPTAN' not in str(item_name).upper():
                                        currency = get_currency(item_price_str)
                                        price_f = clean_price(item_price_str)
                                        if price_f and price_f > 0:
                                            # Senaryo Kontrolü
                                            if has_perakende_header:
                                                kdv_haric = price_f / 1.20 # Senaryo A
                                            else:
                                                kdv_haric = (price_f * 1.35) / 1.20 # Senaryo B (Sadece Toptan/Fiyat)
                                                
                                            clean_name = str(item_name).replace('\n', ' ').strip()
                                            extracted_items_dict[clean_name] = {"name": clean_name, "price": round(kdv_haric, 2), "currency": currency, "source": f"{filename} (PDF)"}
        except Exception as e:
            print(f"HATA PDF ({filename}): {e}")

    elif filename.endswith('.xlsx') or filename.endswith('.xls'):
        try:
            dfs_sup = pd.read_excel(filepath, sheet_name=None) # TUM SAYFALARI OKU
            for sheet_name, df_sup in dfs_sup.items():
                n_col = None
                p_col = None
                has_perakende_eval = False
                
                # Sütun tespiti
                for c in df_sup.columns:
                    c_str = str(c).upper()
                    if 'ÜRÜN' in c_str or 'AÇIKLAMA' in c_str or 'MODEL' in c_str or 'AD' in c_str:
                        if n_col is None: n_col = c
                    if 'PERAKENDE' in c_str or 'PAREKENDE' in c_str or 'PARAKENDE' in c_str:
                        p_col = c
                        has_perakende_eval = True
                    elif ('FİYAT' in c_str or 'TOPTAN' in c_str or 'FİYATI' in c_str) and p_col is None:
                        # Fallback price column
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
                                else: # Toptan zam
                                    kdv_haric = (price_f * 1.35) / 1.20
                                    
                                clean_name = str(item_name).replace('\n', ' ').strip()
                                extracted_items_dict[clean_name] = {"name": clean_name, "price": round(kdv_haric, 2), "currency": currency, "source": f"{filename} - Tab:{sheet_name}"}
        except Exception as e:
            print(f"HATA EXCEL ({filename}): {e}")

extracted_items = list(extracted_items_dict.values())
print(f"Toplam çıkarılan unique ürün adedi: {len(extracted_items)}")

print("Adım 2: Orijinal İdeasoft Excel verisi okunuyor (Sıfırdan inşa süreci)...")
df_main = pd.read_excel(ORIGINAL_EXCEL)
existing_names = df_main['label'].dropna().astype(str).tolist()

matched_count = 0
unmatched_items = []
new_rows = []
price_drop_warnings = []

print("Adım 3: Fuzzy Matching ve Yeni Excel Oluşturuluyor...")

updated_tracker = {}

for item in extracted_items:
    ext_name = item['name']
    match_result = process.extractOne(ext_name, existing_names, scorer=fuzz.token_sort_ratio)
    
    if match_result:
        best_match_name, score = match_result[0], match_result[1]
        if score >= 85:
            current_price_raw = df_main.loc[df_main['label'] == best_match_name, 'price1'].values[0]
            
            try:
                current_price = float(str(current_price_raw).replace(',', '.'))
            except ValueError:
                current_price = 0.0

            if current_price > 0 and item['price'] < current_price:
                price_drop_warnings.append(f"- **DÜŞÜK FİYAT ENGELLENDİ**: '{ext_name}' (Mevcut: {current_price} {item['currency']}, Yeni Gelen: {item['price']} {item['currency']}). Kaynak Liste: {item['source']}")
            else:
                # Güncelle
                df_main.loc[df_main['label'] == best_match_name, 'price1'] = item['price']
                df_main.loc[df_main['label'] == best_match_name, 'currencyAbbr'] = item['currency']
                matched_count += 1
                updated_tracker[best_match_name] = True
        else:
            unmatched_items.append(item)
            new_rows.append({
                'label': ext_name, 'price1': item['price'], 'currencyAbbr': item['currency'], 'status': 1
            })
    else:
        unmatched_items.append(item)
        new_rows.append({
            'label': ext_name, 'price1': item['price'], 'currencyAbbr': item['currency'], 'status': 1
        })


print(f"Eşleşen ve Güncellenen (Var Olan İdeasoft Ürünleri): {matched_count}")
print(f"Eşleşmeyen ve Yepyeni Olarak Eklenen: {len(new_rows)}")

if new_rows:
    df_new = pd.DataFrame(new_rows)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

print("Adım 4: Revize Edilmiş Güncel Excel kaydediliyor...")
try:
    df_main.to_excel(OUTPUT_EXCEL, index=False)
except Exception as e:
    print(f"Excel kaydetme hatası: {e}")

if unmatched_items:
    df_unmatched = pd.DataFrame(unmatched_items)
    df_unmatched.to_csv(UNMATCHED_CSV, index=False, encoding='utf-8')

# Devlog
try:
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (FAZ 3: Düşük Fiyat - Eski Liste Koruması)\n")
        f.write(f"- Çoklu sayfa destekli excel taraması yapıldı, başlığında perakende bulunmayanlara **%35 toptan liste zammı** eklendi.\n")
        f.write(f"- Ekol Voltran ürünleri de dâhil olmak üzere toplam **{len(extracted_items)}** unique (tekil) fiyat işlendi.\n")
        f.write(f"- İdeasoft listesi olan 'prizma-urunler.xlsx' baz alınarak **{matched_count}** ürün en doğru fiyattan güncellendi.\n")
        if price_drop_warnings:
            f.write(f"\n⛔ **DİKKAT! AŞAĞIDAKİ (Tahminen Eski) LİSTELERDEN GELEN DÜŞÜK FİYATLAR İŞLENMEMİŞTİR:** ⛔\n")
            for w in price_drop_warnings:
                f.write(w + "\n")
        f.write(f"- Sistemde bulunmayan **{len(new_rows)}** ürün satırın en altına eklendi.\n")
except Exception as e:
    pass

print("FAZ 3 İŞLEM TAMAMLANDI")

import glob
import pdfplumber
import pandas as pd
import os
import re
from thefuzz import process, fuzz

FILE_PATH = 'prizma-urunler-guncel.xlsx'
df_main = pd.read_excel(FILE_PATH)

def clean_name(n):
    n = str(n).upper()
    n = re.sub(r'AV FİŞEĞİ|FİŞEK|GR\.|GR|,|:', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

existing_series = df_main['label'].dropna()
existing_names = existing_series.tolist()
db_map = {clean_name(name): name for name in existing_names}

pdf_files = sorted(glob.glob('30 mart fiyatlar/*.pdf'))

all_extracted_items = []

print("44 PDF taranıyor, bu işlem biraz zaman alabilir...")

for pdf_path in pdf_files:
    brand_guess = os.path.basename(pdf_path).split()[0].upper()
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                if not tables:
                    text = page.extract_text()
                    if text:
                        lines = [line for line in text.split('\n') if len(line.strip()) > 5]
                        for line in lines:
                            # Heuristic for text lines: find numbers at the end
                            parts = line.split()
                            prices = [p for p in parts if re.search(r'\d+[.,]\d+', p) or '₺' in p]
                            if prices:
                                # longest string part before prices is probably name
                                name_parts = [p for p in parts if p not in prices and not re.search(r'^\d+$', p)]
                                if len(name_parts) >= 2:
                                    name = " ".join(name_parts)
                                    price_str = prices[-1].replace('₺', '').replace('.', '').replace(',', '.')
                                    try:
                                        all_extracted_items.append({
                                            "name": name,
                                            "price_raw": float(price_str),
                                            "source": brand_guess
                                        })
                                    except ValueError:
                                        pass
                else:
                    for table in tables:
                        for row in table:
                            if not row: continue
                            row = [str(cell).replace('\n', ' ').strip() for cell in row if cell]
                            if len(row) < 2: continue
                            
                            longest_str = max(row, key=len)
                            if len(longest_str) < 5 or longest_str.isdigit(): continue
                            
                            prices = []
                            for cell in row:
                                if cell != longest_str:
                                    # find numbers like 15.000,00 or 15000
                                    num_match = re.search(r'[\d.,]+', cell)
                                    if num_match:
                                        clean_num = num_match.group().replace('.', '').replace(',', '.')
                                        # Handle Turkish format: 15.000,00 -> 15000.00
                                        # Actually simple replace covers it mostly but can be wrong if it's 1.500 inside
                                        if clean_num.count('.') > 1:
                                            parts = clean_num.split('.')
                                            clean_num = "".join(parts[:-1]) + "." + parts[-1]
                                        try:
                                            prices.append(float(clean_num))
                                        except:
                                            pass
                            
                            if prices:
                                # usuallyolesale is the lowest price, retail is highest
                                p = min(prices) if min(prices) > 0 else max(prices)
                                if p > 0:
                                    all_extracted_items.append({
                                        "name": longest_str,
                                        "price_raw": p,
                                        "source": brand_guess
                                    })
    except Exception as e:
        print(f"Skipping {os.path.basename(pdf_path)} due to error: {e}")

print(f"Toplam {len(all_extracted_items)} ürün satırı çıkarıldı. Eşleştirme yapılıyor...")

matched_count = 0
new_count = 0
new_rows = []

for item in all_extracted_items:
    # Applying standard pricing logic: Assuming extracted is wholesale list price.
    final_price = round((item['price_raw'] * 1.35) / 1.20, 2)
    
    ext_name_clean = clean_name(item['name'])
    match_result = process.extractOne(ext_name_clean, list(db_map.keys()), scorer=fuzz.token_set_ratio)
    
    if match_result and match_result[1] >= 90: # Very strict deduplication for auto batch
        best_clean = match_result[0]
        original_db_name = db_map[best_clean]
        
        df_main.loc[df_main['label'] == original_db_name, 'price1'] = final_price
        matched_count += 1
    else:
        # Create new
        new_rows.append({
            'label': item['name'],
            'price1': final_price,
            'currencyAbbr': 'TL',
            'status': 1,
            'brand': item['source'],
            'mainCategory': "Yeni Gelen PDF Ürünleri",
            'category': "Kategorize Edilmemiş",
            'subCategory': ""
        })
        new_count += 1
        
if new_rows:
    df_new = pd.DataFrame(new_rows)
    # Just to prevent ballooning from junk text parsing, we take unique names only
    df_new.drop_duplicates(subset=['label'], inplace=True)
    df_main = pd.concat([df_main, df_new], ignore_index=True)

df_main.to_excel(FILE_PATH, index=False)
print(f"Güncellenen (Mükerrer Tespit): {matched_count}, Yepyeni Eklenen Satır: {len(new_rows)}")

# Save raw output just in case
pd.DataFrame(all_extracted_items).to_csv('gecici_pdf_listesi.csv', index=False)

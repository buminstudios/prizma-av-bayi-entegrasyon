"""
UMAREX Fiyat Listesi 30.03 - PSF (Perakende) EUR, KDV Hariç
- Var olan Umarex ürünleri güncellenir
- Yeni ürünler eklenir
- Para birimi: EUR
"""
import pandas as pd
import pdfplumber
import re
import datetime
from thefuzz import fuzz

FILE = 'prizma-urunler-guncel.xlsx'
PDF = 'data/raw/UMAREX FİYAT LİSTESİ 30.03.pdf'

# 1. PDF'den ürünleri çek
products = []
with pdfplumber.open(PDF) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        lines = text.split('\n')
        for line in lines:
            # Format: KOD AÇIKLAMA € TSF € PSF
            # We need to extract the LAST euro value (PSF)
            # Pattern: ... € XX,XX € YY,YY  (or € X.XXX,XX)
            euro_matches = re.findall(r'€\s*([\d.,]+)', line)
            if len(euro_matches) >= 2:
                psf_str = euro_matches[-1].replace('.', '').replace(',', '.')
                try:
                    psf = float(psf_str)
                except:
                    continue
                
                # Extract product name: everything between code and first €
                first_euro_pos = line.find('€')
                if first_euro_pos > 0:
                    prefix = line[:first_euro_pos].strip()
                    # Remove the product code (first token with dots/numbers)
                    code_match = re.match(r'^[\d./-]+\s+', prefix)
                    if code_match:
                        name = prefix[code_match.end():].strip()
                        code = prefix[:code_match.end()].strip()
                    else:
                        name = prefix
                        code = ''
                    
                    if name and psf > 0:
                        products.append({
                            'code': code,
                            'name': name,
                            'psf_eur': psf
                        })

print(f"PDF'den çekilen ürün sayısı: {len(products)}")

# 2. Excel'i yükle
df = pd.read_excel(FILE)

# 3. Mevcut Umarex ürünlerini indexle
umarex_indices = df[df['brand'].astype(str).str.upper().isin(['UMAREX'])].index.tolist()
umarex_labels = {i: str(df.at[i, 'label']).upper() for i in umarex_indices}

def clean_for_match(s):
    s = str(s).upper()
    s = re.sub(r'[^A-ZÇĞİÖŞÜ0-9\s]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

count_updated = 0
count_added = 0
matched_indices = set()

for prod in products:
    name = prod['name']
    psf = prod['psf_eur']
    clean_name = clean_for_match(name)
    
    # Fuzzy match against existing Umarex products
    best_idx = None
    best_score = 0
    
    for idx, lbl in umarex_labels.items():
        if idx in matched_indices:
            continue
        score = fuzz.token_set_ratio(clean_name, clean_for_match(lbl))
        if score > best_score:
            best_score = score
            best_idx = idx
    
    if best_score >= 80 and best_idx is not None:
        # Güncelle
        old_price = df.at[best_idx, 'price1']
        df.at[best_idx, 'price1'] = psf
        df.at[best_idx, 'currencyAbbr'] = 'EUR'
        matched_indices.add(best_idx)
        count_updated += 1
        if count_updated <= 10:
            print(f"[GÜNCELLEME] {df.at[best_idx, 'label']} | {old_price} -> {psf} EUR (skor: {best_score})")
    else:
        # Yeni ürün ekle - kategori belirle
        name_upper = name.upper()
        if any(w in name_upper for w in ['AIRSOFT', '6MM', '6 MM']):
            main_cat = 'Atıcılık & Airsoft'
            cat = 'Airsoft'
            sub = 'Airsoft Tabancalar' if 'TABANCA' in name_upper else ('Airsoft Tüfekler' if 'TÜFEK' in name_upper else 'Airsoft Aksesuarlar')
        elif any(w in name_upper for w in ['HAVALI', 'AIRGUN', '4,5MM', '4.5MM', '5,5MM', 'PCP']):
            main_cat = 'Atıcılık & Airsoft'
            cat = 'Havalı'
            sub = 'Havalı Tabancalar' if 'TABANCA' in name_upper else 'Havalı Tüfekler'
        elif any(w in name_upper for w in ['FENER', 'FENERI']):
            main_cat = 'OPTİK & ELEKTRONİK'
            cat = 'El Feneri & Projektör'
            sub = 'UMAREX'
        elif any(w in name_upper for w in ['ÇAKI', 'BIÇAK']):
            main_cat = 'Av Malzemeleri'
            cat = 'Bıçak & Çakı'
            sub = ''
        elif any(w in name_upper for w in ['DÜRBÜN', 'RED DOT', 'POINTSIGHT', 'MAGNIFIER']):
            main_cat = 'OPTİK & ELEKTRONİK'
            cat = 'Tüfek Dürbünleri'
            sub = ''
        elif any(w in name_upper for w in ['YAY', 'OK ']):
            main_cat = 'Atıcılık & Airsoft'
            cat = 'Okçuluk'
            sub = ''
        elif 'ŞARJÖR' in name_upper:
            main_cat = 'Atıcılık & Airsoft'
            cat = 'Havalı'
            sub = 'Yedek Parça & Aksesuarlar'
        else:
            main_cat = 'Atıcılık & Airsoft'
            cat = 'Aksesuarlar'
            sub = ''
        
        new_row = {
            'label': name,
            'stockCode': prod['code'],
            'brand': 'Umarex',
            'mainCategory': main_cat,
            'category': cat,
            'subCategory': sub,
            'price1': psf,
            'currencyAbbr': 'EUR',
            'tax': 20,
            'stockAmount': 100
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        count_added += 1

print(f"\n=== SONUÇ ===")
print(f"Güncellenen mevcut ürün: {count_updated}")
print(f"Yeni eklenen ürün: {count_added}")

df.to_excel(FILE, index=False)

# Devlog
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Umarex Fiyat Listesi Güncelleme)\n")
    f.write(f"- UMAREX FİYAT LİSTESİ 30.03.pdf işlendi. PSF (Perakende) EUR fiyatları baz alındı (KDV Hariç).\n")
    f.write(f"- Güncellenen mevcut ürün: {count_updated}, Yeni eklenen: {count_added}\n")
    f.write(f"- Para birimi: EUR\n")

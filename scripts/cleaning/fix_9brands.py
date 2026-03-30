"""
9 marka toplu düzeltme: Kategori + Fiyat
Serengeti, Capra, Cheddite, Dağlıoğlu, Hamle, Kariyer, Masai, Odin, Retay
"""
import pandas as pd
import pdfplumber
import re
import datetime
from thefuzz import fuzz

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

def parse_price(s):
    """Parse Turkish price: 16.400,00 or 16400 or 17500"""
    s = str(s).replace('₺', '').replace('TL', '').strip()
    # Remove trailing ,00
    s = re.sub(r',\d{2}$', '', s)
    # Remove dots (thousands sep)
    s = s.replace('.', '').replace(',', '.')
    try: return float(s)
    except: return None

def extract_prices_from_pdf(path):
    """Extract all prices from a PDF, return list of (name, toptan, perakende)"""
    items = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text: continue
            for line in text.split('\n'):
                # Find all numbers that look like prices
                prices = re.findall(r'[\d.,]+', line)
                # Filter to likely prices (4+ digits or has comma/dot pattern)
                price_candidates = []
                for p in prices:
                    val = parse_price(p)
                    if val and val >= 1000:
                        price_candidates.append(val)
                
                if len(price_candidates) >= 2:
                    toptan = price_candidates[-2]
                    perakende = price_candidates[-1]
                    # Remove price parts from line to get name
                    name = line
                    for p in prices:
                        name = name.replace(p, '', 1)
                    name = re.sub(r'[₺TL\s]+', ' ', name).strip()
                    name = re.sub(r'^\d+\s+', '', name).strip()  # Remove leading code
                    if name and len(name) > 3:
                        items.append({'name': name, 'toptan': toptan, 'perakende': perakende})
                elif len(price_candidates) == 1:
                    name = line
                    for p in prices:
                        name = name.replace(p, '', 1)
                    name = re.sub(r'[₺TL\s]+', ' ', name).strip()
                    name = re.sub(r'^\d+\s+', '', name).strip()
                    if name and len(name) > 3:
                        items.append({'name': name, 'toptan': price_candidates[0], 'perakende': price_candidates[0]})
    return items

def clean(s):
    return re.sub(r'[^A-ZÇĞİÖŞÜ0-9\s]', ' ', str(s).upper()).strip()

total_fixed = 0

# ============ SERENGETI ============
print("=== SERENGETI ===")
seren_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/Serengeti Arms 2025 Toptan Fiyat Listesi.pdf')
scount = 0
for i, row in df.iterrows():
    if str(row['brand']) not in ['Serengeti']: continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in seren_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 65:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        scount += 1
        if scount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
print(f"  Toplam: {scount}\n")
total_fixed += scount

# ============ CAPRA ============
print("=== CAPRA ===")
capra_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/CAPRA 2026 FİYAT LİSTESİ.pdf')
ccount = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'CAPRA': continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in capra_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 55:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        # Fix label if too short
        lbl = str(row['label'])
        if 'CAPRA' not in lbl.upper():
            df.at[i, 'label'] = f'CAPRA {lbl}'
        ccount += 1
        if ccount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
    else:
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        ccount += 1
print(f"  Toplam: {ccount}\n")
total_fixed += ccount

# ============ CHEDDITE ============
print("=== CHEDDITE ===")
# Cheddite: 1000'lik fiyat, KDV Hariç. Kutu = 25 (saçma) veya 10 (slug/buckshot)
ched_prices = {}
with pdfplumber.open('data/raw/30 mart fiyatlar/CHEDDİTE FİŞEK FİYAT LİSTESİ.docx 17.12.2025.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text: continue
        for line in text.split('\n'):
            m = re.search(r'([\d.,]+)\s*TL\s*$', line.strip())
            if m:
                raw = m.group(1)
                if re.match(r'^\d{1,3}\.\d{3}$', raw):
                    price = float(raw.replace('.', ''))
                else:
                    price = float(raw.replace(',', '.'))
                name = line[:m.start()].strip()
                name = re.sub(r'^CHD-FSK\d+\s+', '', name).strip()
                ched_prices[name.upper()] = price

chcount = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'Cheddite': continue
    label_clean = clean(row['label'])
    best_key, best_score = None, 0
    for key in ched_prices:
        score = fuzz.token_set_ratio(clean(key), label_clean)
        if score > best_score: best_score, best_key = score, key
    if best_key and best_score >= 60:
        price_1000 = ched_prices[best_key]
        lbl_up = str(row['label']).upper()
        kutu = 10 if any(w in lbl_up for w in ['SLUG', 'BUCKSHOT', 'ŞEVROTİN']) else 25
        final = round(((price_1000 / 1000) * kutu * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        chcount += 1
        print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
print(f"  Toplam: {chcount}\n")
total_fixed += chcount

# ============ DAĞLIOĞLU ============
print("=== DAĞLIOĞLU ===")
dag_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/DAĞLIOĞLU FİYAT LİSTESİ 2025.pdf')
dcount = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'Dağlıoğlu': continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in dag_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 60:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        dcount += 1
        if dcount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
print(f"  Toplam: {dcount}\n")
total_fixed += dcount

# ============ HAMLE ============
print("=== HAMLE ===")
hamle_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/HAMLE SARJORLU 2025 FİYAT LİSTESİ.pdf')
hcount = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'HAMLE': continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in hamle_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 60:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        hcount += 1
        if hcount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
print(f"  Toplam: {hcount}\n")
total_fixed += hcount

# ============ KARIYER ============
print("=== KARİYER ===")
kar_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/KARİYER 2026 FİYAT LİSTESİ.pdf')
kcount = 0
# Kariyer doesn't exist yet, add from PDF
for item in kar_items:
    if item['toptan'] < 5000: continue  # Skip non-gun items
    new_row = {
        'label': f'KARİYER {item["name"]}',
        'brand': 'KARİYER',
        'mainCategory': 'AV TÜFEKLERİ',
        'category': 'YERLİ AV TÜFEKLERİ',
        'subCategory': '',
        'price1': round((item['toptan'] * 1.35) / 1.20, 2),
        'currencyAbbr': 'TL',
        'tax': 20,
        'stockAmount': 100
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    kcount += 1
    if kcount <= 3: print(f"  YENİ: {new_row['price1']} | {new_row['label'][:60]}")
print(f"  Toplam: {kcount}\n")
total_fixed += kcount

# ============ ODIN ============
print("=== ODIN ===")
odin_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/ODIN ARMS 2026 FİYAT LİSTESİ.pdf')
ocount = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'ODIN': continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in odin_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 55:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        lbl = str(row['label'])
        if 'ODIN' not in lbl.upper():
            df.at[i, 'label'] = f'ODIN ARMS {lbl}'
        ocount += 1
        if ocount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
print(f"  Toplam: {ocount}\n")
total_fixed += ocount

# ============ RETAY ============
print("=== RETAY ===")
retay_items = []
with pdfplumber.open('data/raw/30 mart fiyatlar/RETAY HAVALI TÜFEK FİYAT LİSTESİ 2025.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text: continue
        for line in text.split('\n'):
            m = re.search(r'(\d+)\s*TL', line)
            if m:
                price = float(m.group(1))
                name = line[:m.start()].strip()
                name = re.sub(r'^\w+\s+', '', name, count=1).strip()  # Remove barcode
                if name and price >= 500:
                    retay_items.append({'name': name, 'toptan': price})

rcount = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'RETAY': continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in retay_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 65:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'Havalı Tüfekler'
        df.at[i, 'currencyAbbr'] = 'TL'
        rcount += 1
        if rcount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
    else:
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        rcount += 1
print(f"  Toplam: {rcount}\n")
total_fixed += rcount

# ============ MASAI MARA (kategori zaten doğru, fiyat kontrol) ============
print("=== MASAI MARA ===")
masai_items = extract_prices_from_pdf('data/raw/30 mart fiyatlar/MASAI MARA 01.12.2024 TOPTAN FİYAT LİSTESİ.pdf')
mcount = 0
for i, row in df.iterrows():
    if 'Masai' not in str(row['brand']): continue
    label_clean = clean(row['label'])
    best, best_score = None, 0
    for item in masai_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score: best_score, best = score, item
    if best and best_score >= 60:
        final = round((best['toptan'] * 1.35) / 1.20, 2)
        df.at[i, 'price1'] = final
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'currencyAbbr'] = 'TL'
        mcount += 1
        if mcount <= 3: print(f"  {row['price1']} -> {final} | {row['label'][:60]}")
print(f"  Toplam: {mcount}\n")
total_fixed += mcount

print(f"\n=== GENEL TOPLAM: {total_fixed} ürün düzeltildi ===")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (9 Marka Toplu Düzeltme)\n")
    f.write(f"- Serengeti, Capra, Cheddite, Dağlıoğlu, Hamle, Kariyer, Masai Mara, Odin, Retay\n")
    f.write(f"- Toplam {total_fixed} ürün: Kategoriler düzeltildi + PDF listelerinden fiyatlar yeniden hesaplandı.\n")
    f.write(f"- Formül: Toptan (KDV Hariç) * 1.35 / 1.20\n")

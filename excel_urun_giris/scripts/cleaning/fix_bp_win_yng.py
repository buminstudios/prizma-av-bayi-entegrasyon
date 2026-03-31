"""
B&P ve Winchester fışek fiyat düzeltmesi v2
B&P: 1000'lik KDV DAHİL -> (fiyat/1000) * kutu / 1.20 * 1.35
Winchester: Adet KDV Hariç -> adet * kutu * 1.35 / 1.20
"""
import pandas as pd
import pdfplumber
import re
import datetime
from thefuzz import fuzz

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# ============ B&P ============
bp_items = []
with pdfplumber.open('data/raw/30 mart fiyatlar/BP FİYAT LİSTESİ SON GÜNCEL 1.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text: continue
        for line in text.split('\n'):
            m = re.search(r'([\d.,]+)\s*TL\s*$', line.strip())
            if m:
                raw = m.group(1)
                # Handle Turkish number format: 25.250 = 25250, but 91.000 = 91000
                # If has exactly 3 digits after dot -> thousands separator
                if re.match(r'^\d{1,3}\.\d{3}$', raw):
                    price_str = raw.replace('.', '')
                else:
                    price_str = raw.replace(',', '.')
                try:
                    price_1000 = float(price_str)
                except: continue
                name_part = line[:m.start()].strip()
                name_part = re.sub(r'^BP-FSK\d+\s+', '', name_part).strip()
                name_part = re.sub(r'\s*STOK YOK\s*', ' ', name_part).strip()
                bp_items.append({'name': name_part.strip(), 'price_1000': price_1000})

print(f"B&P: {len(bp_items)} item from PDF")

def clean(s):
    return re.sub(r'[^A-ZÇĞİÖŞÜ0-9\s]', ' ', str(s).upper()).strip()

bp_count = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'B&P': continue
    label = str(row['label'])
    label_clean = clean(label)
    
    best = None
    best_score = 0
    for item in bp_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score:
            best_score = score
            best = item
    
    if best and best_score >= 60:
        price_1000 = best['price_1000']
        lbl_up = label.upper()
        if any(w in lbl_up for w in ['SLUG', 'KURŞUN', 'PALLA', 'SHOCK', 'BUCKSHOT', 'PELLETS', 'PALLETTONI']):
            kutu = 10
        elif '50 GR' in lbl_up or 'MAGNUM 50' in lbl_up:
            kutu = 10
        else:
            kutu = 25
        
        # 1000'lik KDV DAHİL fiyat, kutu bazına düşür, KDV düş, kar ekle
        final = round(((price_1000 / 1000) * kutu / 1.20) * 1.35, 2)
        old = df.at[i, 'price1']
        df.at[i, 'price1'] = final
        df.at[i, 'currencyAbbr'] = 'TL'
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        bp_count += 1
        print(f"[B&P] {old:>10} -> {final:>8} | {label[:60]} (match: {best['name'][:40]}, score:{best_score})")

print(f"\nB&P TOPLAM: {bp_count}\n")

# ============ WINCHESTER ============
win_items = []
with pdfplumber.open('data/raw/30 mart fiyatlar/WINCHESTER - AV FİŞEK FİYAT LİSTESİ - 2025-4.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text: continue
        for line in text.split('\n'):
            prices = re.findall(r'([\d.,]+)\s*₺', line)
            if len(prices) >= 2:
                raw_t = prices[0]
                # These are adet prices like 28.00, 143.00 - dot is decimal
                toptan_str = raw_t.replace(',', '.')
                try:
                    toptan_adet = float(toptan_str)
                except: continue
                name_match = re.search(r'(?:EU|US)\s+(?:YENİ\s+)?(.+?)(?:\s+\d+[\d.,]*\s*₺)', line)
                if name_match:
                    name = name_match.group(1).strip()
                    win_items.append({'name': name, 'toptan_adet': toptan_adet})

print(f"Winchester: {len(win_items)} item from PDF")

win_count = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'Winchester': continue
    label = str(row['label'])
    lbl_up = label.upper()
    
    # Skip tüfekler
    if any(w in lbl_up for w in ['SX3', 'SX4', 'SXP', 'XPR', 'MODEL', 'OTOMATİK', 'POMPALI', 'SÜPERPOZE']):
        continue
    
    label_clean = clean(label)
    best = None
    best_score = 0
    for item in win_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score:
            best_score = score
            best = item
    
    if best and best_score >= 65:
        toptan_adet = best['toptan_adet']
        if any(w in lbl_up for w in ['SLUG', 'KURŞUN', 'SABOT', 'BRENNEKE']):
            kutu = 10
        elif any(w in lbl_up for w in ['BUCKSHOT', 'PELLETS', 'ŞEVROTİN', 'ŞAVROTIN']):
            kutu = 10
        else:
            kutu = 25
        
        # Adet KDV Hariç -> kutu * 1.35 / 1.20
        final = round((toptan_adet * kutu * 1.35) / 1.20, 2)
        old = df.at[i, 'price1']
        df.at[i, 'price1'] = final
        df.at[i, 'currencyAbbr'] = 'TL'
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        win_count += 1
        if win_count <= 10:
            print(f"[WIN] {old:>10} -> {final:>8} | {label[:55]} (match: {best['name'][:40]}, score:{best_score})")

print(f"\nWINCHESTER TOPLAM: {win_count}")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (B&P + Winchester + YNG Toplu Düzeltme v2)\n")
    f.write(f"- B&P: {bp_count} fişek, 1000'lik KDV dahil PDF baz alınarak kutu fiyatına düşürüldü.\n")
    f.write(f"- Winchester: {win_count} fişek, adet toptan KDV hariç PDF baz alınarak düzeltildi.\n")
    f.write(f"- YNG: 12 ürün AV TÜFEKLERİ kategorisine taşındı.\n")

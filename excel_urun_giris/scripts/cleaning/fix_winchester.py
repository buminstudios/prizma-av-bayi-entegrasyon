"""
Winchester fişek fiyat düzeltmesi
- Kategori: Tümü AV FİŞEKLERİ
- Fiyat: PDF'den toptan KDV hariç * 1.35 / 1.20
"""
import pandas as pd
import pdfplumber
import re
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# PDF'den fiyat haritası çıkar
price_map = {}  # model -> toptan_kdv_haric
with pdfplumber.open('data/raw/30 mart fiyatlar/WINCHESTER - AV FİŞEK FİYAT LİSTESİ - 2025-4.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        for line in text.split('\n'):
            # Format: KOD MENŞE MODEL TOPTAN KDV_DAHIL PERAKENDE
            # Find model name (Winchester ...)
            m = re.search(r'((?:YENİ\s+)?Winchester\s+.+?)\s+(\d+[\.,]\d+)\s+₺', line)
            if m:
                model = m.group(1).strip()
                price_str = m.group(2).replace('.', '').replace(',', '.')
                try:
                    toptan = float(price_str)
                except:
                    continue
                price_map[model.upper()] = toptan

print(f'PDF\'den {len(price_map)} ürün okundu')

# Winchester fişek ürünlerini güncelle
count = 0
for i, row in df.iterrows():
    if 'Winchester' not in str(row['brand']) and 'WINCHESTER' not in str(row['brand']).upper():
        continue
    label = str(row['label'])
    
    # Tüfek ürünlerini atla (SX3, SX4, SXP, Select Light)
    if any(x in label for x in ['SX3', 'SX4', 'SXP', 'Select Light', 'Süperpoze', 'Pompalı']):
        continue
    
    # Kategoriyi AV FİŞEKLERİ yap
    df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
    
    # Fiyat eşleştir
    label_up = label.upper()
    best_key, best_len = None, 0
    for key in price_map:
        # Remove YENİ prefix for matching
        key_clean = key.replace('YENİ ', '').strip()
        label_clean = label_up.replace('YENİ ', '').strip()
        if key_clean in label_clean and len(key_clean) > best_len:
            best_key, best_len = key, len(key_clean)
    
    if not best_key:
        # Fuzzy match on key words
        from thefuzz import fuzz
        best_score = 0
        for key in price_map:
            score = fuzz.token_set_ratio(key, label_up)
            if score > best_score:
                best_score = score
                best_key = key
        if best_score < 75:
            best_key = None
    
    if best_key:
        toptan = price_map[best_key]
        final = round((toptan * 1.35) / 1.20, 2)
        old = df.at[i, 'price1']
        df.at[i, 'price1'] = final
        df.at[i, 'currencyAbbr'] = 'TL'
        count += 1
        if abs(old - final) > 10:
            print(f'{old:>10} -> {final:>8} | {label[:60]}')

print(f'\nWinchester fişek düzeltilen: {count}')

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Winchester Fişek Düzeltme)\n")
    f.write(f"- {count} Winchester fişek: kategori AV FİŞEKLERİ + fiyat düzeltildi.\n")
    f.write(f"- Formül: Toptan KDV Hariç * 1.35 / 1.20\n")

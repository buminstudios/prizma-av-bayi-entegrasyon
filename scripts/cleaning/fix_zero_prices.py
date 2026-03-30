"""
Kapsamlı Sıfır Fiyat Düzeltici
Strateji:
1. Aynı markada aynı gram/kalibreye sahip fiyatlı ürünü referans al
2. Referans bulunamazsa, aynı markadaki fiyatlı ürünlerin medyanını kullan
3. Powerdex için yeni listeden stok kod eşleştirmesi yap
4. Silah/tüfek gibi yüksek fiyatlı ürünlerde medyan yaklaşımı uygula
"""
import pandas as pd
import datetime
import re

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# --- POWERDEX: Stok kodu ile yeni listeden eşleştir ---
try:
    df_pd = pd.read_excel('data/raw/powerdex fener.xlsx', header=3)
    pd_price_map = {}
    for _, row in df_pd.iterrows():
        kod = str(row['ÜRÜN KODU']).strip()
        price_raw = str(row['ÜRÜN FİYATI']).replace('$', '').replace(',', '').strip()
        if kod != 'nan' and price_raw != 'nan':
            try:
                pd_price_map[kod.upper()] = float(price_raw) * 2.0  # Kullanıcı kuralı: *2
            except:
                pass
    print(f"Powerdex price map loaded: {len(pd_price_map)} items")
except Exception as e:
    pd_price_map = {}
    print(f"Powerdex list not found: {e}")

# --- Fişek gram/kalibre eşleyici ---
def extract_gram(label):
    m = re.search(r'(\d+)\s*GR', str(label).upper())
    return int(m.group(1)) if m else None

def extract_calibre(label):
    lbl = str(label).upper()
    for c in ['12', '16', '20', '24', '28', '32', '36']:
        if f'{c} CAL' in lbl or f'{c} ÇAP' in lbl:
            return c
    return None

def is_slug(label):
    lbl = str(label).upper()
    return any(w in lbl for w in ['SLUG', 'KURŞUN', 'SABOT'])

def is_buckshot(label):
    lbl = str(label).upper()
    return any(w in lbl for w in ['BUCKSHOT', 'ŞEVROTİN', 'PELLETS', '11/0', '7/0'])

# Build reference maps per brand
brand_refs = {}
for i, row in df.iterrows():
    if float(row['price1']) > 0:
        brand = str(row['brand'])
        if brand not in brand_refs:
            brand_refs[brand] = []
        brand_refs[brand].append(row)

count_fixed = 0
fixes_log = []

for i, row in df.iterrows():
    if float(row['price1']) > 0:
        continue
    
    brand = str(row['brand'])
    label = str(row['label'])
    lbl_upper = label.upper()
    
    new_price = None
    method = ''
    
    # 1. Powerdex: stok kodu eşleştir
    if brand == 'POWERDEX':
        # Extract PD-XXXX from label
        m = re.search(r'PD-?\d+', lbl_upper)
        if m:
            kod = m.group(0).replace(' ', '')
            if kod in pd_price_map:
                new_price = pd_price_map[kod]
                method = f'Powerdex liste (*2): {kod}'
    
    # 2. Fişek markaları: gram + kalibre eşleştirmesi
    if new_price is None and brand in brand_refs:
        gram = extract_gram(label)
        cal = extract_calibre(label)
        slug = is_slug(label)
        buck = is_buckshot(label)
        
        refs = brand_refs[brand]
        
        # Öncelik 1: Aynı tür (slug/buckshot/saçma) + aynı gram + aynı kalibre
        for ref in refs:
            ref_lbl = str(ref['label']).upper()
            ref_gram = extract_gram(ref['label'])
            ref_cal = extract_calibre(ref['label'])
            ref_slug = is_slug(ref['label'])
            ref_buck = is_buckshot(ref['label'])
            
            if slug and ref_slug and cal == ref_cal:
                new_price = float(ref['price1'])
                method = f'Slug benzer: {ref["label"]}'
                break
            elif buck and ref_buck and cal == ref_cal:
                new_price = float(ref['price1'])
                method = f'Buckshot benzer: {ref["label"]}'
                break
            elif gram and ref_gram and gram == ref_gram and cal == ref_cal and not slug and not buck and not ref_slug and not ref_buck:
                new_price = float(ref['price1'])
                method = f'Gram+Cal eşleşme: {ref["label"]}'
                break
        
        # Öncelik 2: Sadece gram eşleşmesi (farklı kalibre olsa da)
        if new_price is None:
            for ref in refs:
                ref_gram = extract_gram(ref['label'])
                ref_slug = is_slug(ref['label'])
                ref_buck = is_buckshot(ref['label'])
                if slug and ref_slug:
                    new_price = float(ref['price1'])
                    method = f'Slug genel: {ref["label"]}'
                    break
                elif buck and ref_buck:
                    new_price = float(ref['price1'])
                    method = f'Buckshot genel: {ref["label"]}'
                    break
                elif gram and ref_gram and gram == ref_gram and not slug and not buck and not ref_slug and not ref_buck:
                    new_price = float(ref['price1'])
                    method = f'Gram eşleşme: {ref["label"]}'
                    break
        
        # Öncelik 3: Marka medyanı (son çare)
        if new_price is None:
            prices = [float(r['price1']) for r in refs if float(r['price1']) > 0]
            if prices:
                # Filter out outliers (tüfek fiyatları vs fişek fiyatları karışmasın)
                # Fişek markaları için sadece düşük fiyatlı ürünleri al
                fisek_brands = ['Zuber','Sterling','Mirage','YAF','Fiocchi','Meca','Kaiser','BPS','Lambro',
                                'Sellier & Bellot','Federal','Rottweil','B&P','RC','Remington','Winchester',
                                'Jet','Cheddite','Saga','Rio','Özkursan','Bornaghi','Dionisi','Codex',
                                'Geco','Imperial','Eley','Apport','Glavpatron','Mesco']
                if brand in fisek_brands:
                    prices = [p for p in prices if p < 5000]  # Fişek 5000 TL'den pahalı olamaz
                
                if prices:
                    median = sorted(prices)[len(prices) // 2]
                    new_price = median
                    method = f'Marka medyanı: {median:.0f} TL ({len(prices)} referans)'
    
    # Fiyat ata
    if new_price is not None and new_price > 0:
        # Fiyatı mantıklılık kontrolü: çok yüksekse (100K+) veya çok düşükse (0.01) atla
        if new_price < 0.5 or new_price > 200000:
            continue
        df.at[i, 'price1'] = round(new_price, 2)
        count_fixed += 1
        fixes_log.append(f"[{brand}] {label} -> {new_price:.2f} ({method})")

# Rapor
print(f"\n=== SONUÇ ===")
print(f"Düzeltilen ürün: {count_fixed}")
remaining = len(df[df['price1'].astype(float) <= 0])
print(f"Hala sıfır fiyatlı: {remaining}")

for log in fixes_log[:20]:
    print(log)
if len(fixes_log) > 20:
    print(f"... ve {len(fixes_log) - 20} daha")

df.to_excel(FILE, index=False)

# Devlog
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Kapsamlı Sıfır Fiyat Düzeltmesi)\n")
    f.write(f"- Veritabanındaki 528 adet fiyatı 0.00 olan ürün tespit edildi.\n")
    f.write(f"- Akıllı eşleştirme: Aynı marka+gram+kalibre referansı, slug/buckshot türü eşleştirmesi ve marka medyanı yöntemleriyle {count_fixed} ürüne fiyat atandı.\n")
    f.write(f"- Powerdex ürünleri yeni listeden stok kodu eşleştirmesiyle güncellendi.\n")
    f.write(f"- Kalan sıfır fiyatlı ürün: {remaining}\n")

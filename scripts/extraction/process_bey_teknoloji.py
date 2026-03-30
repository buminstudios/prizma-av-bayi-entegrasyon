"""
Bey Teknoloji - Perakende KDV Dahil fiyatlarıyla 8 eksik sayfa ekleme
+ Mevcut Vortex/Riton/GPO fiyatlarını da perakende KDV dahil ile güncelle
"""
import pandas as pd
import datetime

SOURCE = 'data/raw/ürünler fiyatlar/2026 NAKİT YETKİLİ BAYİ BEY TEKNOLOJİ 2026.xlsx'
FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
xls = pd.ExcelFile(SOURCE)

# Önce yanlış eklenen 723 ürünü sil
brands_to_remove = ['Element Optics', 'Bushnell', 'Nutrek', 'Discovery Optics', 
                     'Harris', 'Skywoods', 'Primos', 'HorusCam']
before = len(df)
df = df[~df['brand'].isin(brands_to_remove)]
df = df.reset_index(drop=True)
print(f'Silinen: {before - len(df)}')

total_added = 0

# Sayfa yapıları: (sheet_name, brand, mainCat, cat, model_col, perakende_col, data_start_row)
sheets = [
    ('ELEMET YENİ',  'Element Optics',  'DÜRBÜN & OPTİK', 'Tüfek Dürbünleri', 1, 7, 5),
    ('BUSHNELL',     'Bushnell',        'DÜRBÜN & OPTİK', 'Tüfek Dürbünleri', 2, 6, 9),
    ('NUTREK ',       'Nutrek',          'DÜRBÜN & OPTİK', 'Tüfek Dürbünleri', 1, 6, 7),
    ('DİSCOVERYOP',  'Discovery Optics','DÜRBÜN & OPTİK', 'Tüfek Dürbünleri', 1, 5, 7),
    ('HARRIS',       'Harris',          'DÜRBÜN & OPTİK', 'Bipod & Aksesuar',  1, 6, 7),
    ('SKYWOODS',     'Skywoods',        'DÜRBÜN & OPTİK', 'Fener & Aksesuar',  1, 5, 6),
    ('PİRİMOS ',     'Primos',          'AV AKSESUARLARI', 'Av Aksesuarları',   1, 5, 6),
    ('HORUSCAM2023', 'HorusCam',        'AV AKSESUARLARI', 'Fotokapanlar',      1, 4, 4),
]

for sheet_name, brand, main_cat, category, model_col, perakende_col, start_row in sheets:
    raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
    count = 0
    for idx in range(start_row, len(raw)):
        row = raw.iloc[idx]
        
        # Model
        model = str(row.iloc[model_col]).strip() if model_col < len(row) and pd.notna(row.iloc[model_col]) else ''
        if not model or model == 'nan' or len(model) < 3:
            continue
        
        # SKU/KOD (col 0) for Harris/Skywoods
        kod = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
        
        # Perakende KDV Dahil
        price = row.iloc[perakende_col] if perakende_col < len(row) and pd.notna(row.iloc[perakende_col]) else None
        if not price:
            continue
        try:
            price = float(price)
        except:
            continue
        if price < 5:
            continue
        
        # Label
        if brand in ['Harris', 'Skywoods'] and kod and kod != 'nan':
            label = f'{brand} {kod} {model}'
        elif brand.upper() not in model.upper():
            label = f'{brand} {model}'
        else:
            label = model
        
        # Check dupe
        if label in df['label'].values:
            continue
        
        new_row = {
            'label': label,
            'brand': brand,
            'mainCategory': main_cat,
            'category': category,
            'subCategory': '',
            'price1': round(price, 2),
            'currencyAbbr': 'EUR',
            'tax': 20,
            'stockAmount': 100,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        count += 1
    
    total_added += count
    print(f'[{brand}] {count} ürün eklendi (perakende KDV dahil)')

# === Mevcut Vortex, Riton, GPO fiyatlarını da perakende KDV dahil ile güncelle ===
update_sheets = [
    ('VORTEX YENİ', 'Vortex', 1, 5, 10),  # model col 1, perakende col 5, start row 10
    ('RİTON ',      'Riton',  1, 5, 5),    # model col 1, perakende col 5, start row 5
    ('GPO',         'GPO',    1, 6, 9),    # model col 1, perakende col 6, start row 9 
]

for sheet_name, brand_search, model_col, perakende_col, start_row in update_sheets:
    raw = pd.read_excel(xls, sheet_name=sheet_name, header=None)
    
    # Build price map: model -> perakende
    price_map = {}
    for idx in range(start_row, len(raw)):
        row = raw.iloc[idx]
        model = str(row.iloc[model_col]).strip() if model_col < len(row) and pd.notna(row.iloc[model_col]) else ''
        price = row.iloc[perakende_col] if perakende_col < len(row) and pd.notna(row.iloc[perakende_col]) else None
        if model and model != 'nan' and price:
            try:
                price_map[model.upper()] = float(price)
            except:
                pass
    
    # Update existing
    ucount = 0
    for i, row in df.iterrows():
        if brand_search.lower() not in str(row['brand']).lower():
            continue
        label_up = str(row['label']).upper()
        
        best_key, best_len = None, 0
        for key, price in price_map.items():
            if key in label_up and len(key) > best_len:
                best_key, best_len = key, len(key)
        
        if best_key:
            new_price = round(price_map[best_key], 2)
            old = df.at[i, 'price1']
            df.at[i, 'price1'] = new_price
            df.at[i, 'currencyAbbr'] = 'EUR'
            ucount += 1
    
    print(f'[{brand_search} güncelleme] {ucount} ürün perakende KDV dahil ile güncellendi')

print(f'\n=== TOPLAM YENİ: {total_added}, VERİTABANI: {len(df)} ===')

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Bey Teknoloji - Perakende KDV Dahil)\n")
    f.write(f"- 8 eksik sayfa eklendi: Element, Bushnell, Nutrek, DiscoveryOP, Harris, Skywoods, Primos, HorusCam\n")
    f.write(f"- Toplam {total_added} yeni ürün. Fiyat: Perakende KDV Dahil (EUR)\n")
    f.write(f"- Vortex, Riton, GPO fiyatları da perakende KDV dahil ile güncellendi.\n")

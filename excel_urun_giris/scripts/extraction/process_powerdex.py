import pandas as pd
import datetime

df_main = pd.read_excel('prizma-urunler-guncel.xlsx')
df_new = pd.read_excel('data/raw/powerdex fener.xlsx', header=3)

added_products = []
count_added = 0
count_skipped = 0

# To speed up checking, we can use exact matches or contains. But since DB is 4000 rows, iteration string match is fine.
main_labels = df_main['label'].astype(str).str.upper().tolist()
main_codes = df_main['stockCode'].astype(str).str.upper().tolist()

for i, row in df_new.iterrows():
    kod = str(row['ÜRÜN KODU']).strip()
    name = str(row['ÜRÜN CİNSİ']).strip()
    price_raw = str(row['ÜRÜN FİYATI']).replace('$', '').replace(',', '').strip()
    
    if kod == 'nan' or name == 'nan' or price_raw == 'nan':
        continue
    
    # Check if exists (olmasını engellemek için)
    # Check if kod is a substring in any stockCode, or name is in any label.
    kod_upper = kod.upper()
    name_upper = name.upper()
    
    # Many items might have same kod prefix, so let's do exact or strong match for kod
    # For name, we can do substring match
    exists = False
    for ml in main_labels:
        if name_upper in ml or kod_upper in ml:
            exists = True
            break
            
    if not exists:
        for mc in main_codes:
            if kod_upper == mc:
                exists = True
                break
                
    if exists:
        count_skipped += 1
        continue
        
    try:
        price_float = float(price_raw)
    except ValueError:
        continue
        
    # Sadece fiyatı * 2 yapacağız
    final_price = price_float * 2.0
    
    new_row = pd.Series({
        'label': name,
        'stockCode': kod,
        'brand': 'POWERDEX',
        'mainCategory': 'OPTİK & ELEKTRONİK',
        'category': 'El Feneri & Projektör',
        'subCategory': 'POWERDEX',
        'price1': final_price,
        'currencyAbbr': 'USD',
        'tax': 20,
        'stockAmount': 100
    })
    
    df_main = pd.concat([df_main, pd.DataFrame([new_row])], ignore_index=True)
    count_added += 1
    added_products.append(name)

df_main.to_excel('prizma-urunler-guncel.xlsx', index=False)

print(f"Skipped (Already exists): {count_skipped}")
print(f"Added New Products: {count_added}")

# log
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Powerdex Fiyat Entegrasyonu)\n")
    f.write(f"- 'powerdex fener.xlsx' okundu. Var olan modeller fiyat/stok EZİLMEDEN atlandı.\n")
    f.write(f"- Olmayan yepyeni model sayısı: {count_added} sisteme eklendi.\n")
    f.write(f"- Kural: Yeni Liste Fiyatı * 2 (KDV Hariç %20 olarak kaydedildi)\n")

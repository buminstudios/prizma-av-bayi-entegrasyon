"""
Bornaghi Fişek Fiyat Düzeltmesi - PDF'den doğru fiyatlar
Kaynak: BORNAGHI-FISEK FIYAT LISTESI 25-3.pdf
Kural: Toptan Adet Fiyatı (KDV Hariç) * Kutu Adeti * 1.35 / 1.20
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# PDF'den okunan Bornaghi fiyatları (Toptan Adet/TL KDV Hariç)
bornaghi_prices = [
    # (anahtar kelimeler, toptan_adet_tl, kutu)
    ("BIOR 30", "30 GR", "12", 19.50, 25),
    ("GAME 30", "30 GR", "16", 22.50, 25),
    ("DISPERSANTE", "34 GR", "12", 25.50, 25),
    ("MAGNUM 50", "50 GR", "12", 43.00, 10),
    ("DELUXE 28", "28 GR", "12", 19.00, 25),
    ("DELUXE 32", "32 GR", "12", 21.50, 25),
    ("DELUXE 34", "34 GR", "12", 22.50, 25),
    ("DELUXE 36", "36 GR", "12", 29.00, 25),
    ("FELT 33", "33 GR", "12", 27.50, 25),
    ("PELLETS", "11/0", "12", 38.00, 10),
    ("SLUG", "SLUG", "20", 54.00, 10),
    ("SLUG", "SLUG", "12", 58.00, 10),
    ("SLUG", "SLUG", "36", 48.00, 10),
    ("GAME 25", "25 GR", "20", 22.00, 25),
    ("SEMI MAGNUM", "32 GR", "20", 31.00, 25),
    ("EXTRA 14", "14 GR", "36", 25.50, 25),
    ("EXTRA 35", "35 GR", "12", 27.50, 25),
    ("SPORT 24", "24 GR", "12", 17.00, 25),
]

count = 0
for i, row in df.iterrows():
    if str(row['brand']) != 'Bornaghi':
        continue
    
    label = str(row['label']).upper()
    matched = False
    
    for keywords, gram_key, cal_key, adet_tl, kutu in bornaghi_prices:
        kw_upper = keywords.upper()
        # Match: label must contain the keywords AND caliber
        if kw_upper in label and f'{cal_key} CAL' in label:
            kutu_fiyat = adet_tl * kutu
            final = round((kutu_fiyat * 1.35) / 1.20, 2)
            old = df.at[i, 'price1']
            df.at[i, 'price1'] = final
            df.at[i, 'currencyAbbr'] = 'TL'
            print(f"[{old} -> {final}] {row['label']}")
            count += 1
            matched = True
            break
    
    if not matched:
        # Fallback: gram bazlı eşleştirme
        for keywords, gram_key, cal_key, adet_tl, kutu in bornaghi_prices:
            if gram_key in label:
                kutu_fiyat = adet_tl * kutu
                final = round((kutu_fiyat * 1.35) / 1.20, 2)
                old = df.at[i, 'price1']
                df.at[i, 'price1'] = final
                df.at[i, 'currencyAbbr'] = 'TL'
                print(f"[{old} -> {final}] {row['label']} (gram fallback)")
                count += 1
                break

print(f"\nDüzeltilen Bornaghi: {count}")
df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Bornaghi Fişek Fiyat Düzeltmesi)\n")
    f.write(f"- BORNAGHI-FISEK FIYAT LISTESI 25-3.pdf baz alınarak {count} ürünün fiyatı düzeltildi.\n")
    f.write(f"- Formül: Toptan Adet (KDV Hariç) * Kutu Adeti * 1.35 / 1.20\n")

"""
Winchester Fişek Fiyat Düzeltme
PDF: Tavsiye Edilen Perakende (KDV Dahil) - ADET fiyatı
"""
import pandas as pd
import pdfplumber
import re
import datetime
from thefuzz import fuzz

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# PDF'den fiyatları çek
win_items = []
with pdfplumber.open('data/raw/30 mart fiyatlar/WINCHESTER - AV FİŞEK FİYAT LİSTESİ - 2025-4.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue
        for line in text.split('\n'):
            # 3 fiyat sütunu: Toptan KDV Hariç | Toptan KDV Dahil | Tavsiye Perakende
            prices = re.findall(r'([\d.,]+)\s*₺', line)
            if len(prices) >= 3:
                # Üçüncü fiyat = Tavsiye Edilen Perakende (KDV Dahil)
                raw_perakende = prices[2]
                perakende_str = raw_perakende.replace(',', '.').replace(' ', '')
                try:
                    perakende = float(perakende_str)
                except:
                    continue
                
                # Ürün adı
                name_match = re.search(r'(?:EU|USA)\s+(?:YENİ\s+)?(.+?)(?:\s+[\d.,]+\s*₺)', line)
                if name_match:
                    name = name_match.group(1).strip()
                    win_items.append({
                        'name': name,
                        'perakende': perakende  # ADET fiyatı
                    })

print(f"PDF'den {len(win_items)} Winchester fişek okundu")
print("İlk 5 örnek:")
for item in win_items[:5]:
    print(f"  {item['name'][:55]:55s} | {item['perakende']:>8} TL/adet")

# Temizleme fonksiyonu
def clean(s):
    return re.sub(r'[^A-ZÇĞİÖŞÜ0-9\s]', ' ', str(s).upper()).strip()

# Tüm Winchester fişekleri güncelle
win_mask = (
    df['brand'].astype(str).str.upper().str.contains('WINCHESTER', na=False) &
    df['mainCategory'].astype(str).str.contains('FİŞEK', na=False)
)

updated = 0
not_matched = 0
for i in df[win_mask].index:
    label = str(df.at[i, 'label'])
    label_clean = clean(label)
    
    best = None
    best_score = 0
    for item in win_items:
        score = fuzz.token_set_ratio(clean(item['name']), label_clean)
        if score > best_score:
            best_score = score
            best = item
    
    if best and best_score >= 65:
        old_price = df.at[i, 'price1']
        new_price = best['perakende']  # Tavsiye edilen perakende ADET fiyatı
        df.at[i, 'price1'] = new_price
        df.at[i, 'currencyAbbr'] = 'TL'
        updated += 1
        print(f"  {old_price:>10} -> {new_price:>8} TL | {label[:55]} (match: {best['name'][:40]}, skor:{best_score})")
    else:
        not_matched += 1
        print(f"  ESLESEMEDI: {label[:60]} (en iyi skor: {best_score})")

print(f"\nGuncellenen: {updated}")
print(f"Eslesmeyen: {not_matched}")

# Kaydet
df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Winchester Fisek Fiyat Duzeltme)\n")
    f.write(f"- {updated} Winchester fisegin fiyati PDF'den 'Tavsiye Edilen Perakende (KDV Dahil)' adet fiyati olarak guncellendi.\n")
    f.write(f"- Onceki fiyatlar hatali formulle hesaplanmisti.\n")
    f.write(f"- Eslesmeyen: {not_matched}\n")

print("\nKaydedildi!")

"""
Sarsılmaz Güncel Fiyat Listesi - 1.05.2026
Kaynak: Ekran görüntüsünden okundu
Fiyatlar: Toptan, KDV Hariç
Formül: Toptan * 1.35 / 1.20
"""
import pandas as pd
import datetime
from thefuzz import fuzz
import re

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

sarsilmaz_prices = [
    # Yarı Otomatik Av Tüfekleri
    ("SA-X 700 12-20 Cal.", 27750),
    ("SA-W 700 12-20 Cal.", 29000),
    ("SA-W 700 L", 29500),
    ("SA-W 700 S", 29750),
    ("SA-W 700 LX", 31000),
    ("SA-W 700 DE LUXE", 32000),
    ("SA-W 700 DE LUXE S", 32000),
    ("MAGIC SİYAH", 32750),
    ("MAGIC BEYAZ", 33500),
    ("MAGIC BRONZE", 33500),
    ("MAGIC SLUG SİYAH", 41000),
    ("MAGIC SLUG BEYAZ", 41750),
    ("MAGIC SLUG SİYAH CANTILEVER", 42500),
    ("MAGIC COMBO SİYAH", 46750),
    ("MAGIC COMBO BEYAZ", 48250),
    ("MAGIC COMBO 2023", 41250),
    ("VERTU SİYAH", 38000),
    ("VERTU BEYAZ", 38500),
    ("VERTU SLUG SİYAH", 41500),
    ("VERTU SLUG BEYAZ", 42500),
    ("FRANCHI İngiliz Kundak", 39250),
    ("FRANCHI FIRST CLASS", 36000),
    # Yarı Otomatik Taktical
    ("DRONE KILLER DK12 SİYAH", 39000),
    ("DRONE KILLER DK12 TUNGSTEN", 39000),
    ("DRONE KILLER DK12 BRONZ", 39000),
    ("DRONE KILLER DK12 HAKİ", 39000),
    # Pompalı Tüfekler
    ("M204 STD", 17500),
    ("M204 ATP TABANCA KABZE", 17750),
    ("M204 P TELESKOPİK DİPÇ", 17750),
    ("M206 W TABANCA KABZE", 18250),
    ("M208 TAB KAB TELK DİPÇ", 18750),
    ("M212", 22500),
]

def clean(s):
    return re.sub(r'[^A-ZÇĞİÖŞÜ0-9\s]', ' ', str(s).upper()).strip()

count_updated = 0
count_added = 0

for name, toptan in sarsilmaz_prices:
    final = round((toptan * 1.35) / 1.20, 2)
    name_clean = clean(name)
    
    # Fuzzy match against existing Sarsılmaz
    best_idx = None
    best_score = 0
    for i, row in df.iterrows():
        if 'arsılmaz' not in str(row['brand']) and 'ARSILMAZ' not in str(row['brand']).upper():
            continue
        score = fuzz.token_set_ratio(name_clean, clean(row['label']))
        if score > best_score:
            best_score = score
            best_idx = i
    
    if best_score >= 70 and best_idx is not None:
        old = df.at[best_idx, 'price1']
        df.at[best_idx, 'price1'] = final
        df.at[best_idx, 'currencyAbbr'] = 'TL'
        df.at[best_idx, 'mainCategory'] = 'AV TÜFEKLERİ'
        count_updated += 1
        print(f"[GÜNCELLENDİ] {old:>12} -> {final:>10} | {df.at[best_idx, 'label'][:60]} (skor:{best_score})")
    else:
        # Yeni ürün ekle
        cat = 'Pompalı Av Tüfekleri' if 'M2' in name else 'Yarımotomatik Av Tüfekleri'
        new_row = {
            'label': f'Sarsılmaz {name} Av Tüfeği',
            'brand': 'Sarsılmaz',
            'mainCategory': 'AV TÜFEKLERİ',
            'category': cat,
            'subCategory': '',
            'price1': final,
            'currencyAbbr': 'TL',
            'tax': 20,
            'stockAmount': 100,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        count_added += 1
        print(f"[YENİ]        -> {final:>10} | Sarsılmaz {name} (best_score:{best_score})")

print(f"\n=== SONUÇ ===")
print(f"Güncellenen: {count_updated}")
print(f"Yeni eklenen: {count_added}")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Sarsılmaz Fiyat Güncelleme)\n")
    f.write(f"- Sarsılmaz 1.05.2026 tarihli güncel fiyat listesi uygulandı.\n")
    f.write(f"- {count_updated} ürün güncellendi, {count_added} yeni ürün eklendi.\n")
    f.write(f"- Drone Killer DK12 serisi yeni giriş.\n")
    f.write(f"- Formül: Toptan (KDV Hariç) * 1.35 / 1.20\n")

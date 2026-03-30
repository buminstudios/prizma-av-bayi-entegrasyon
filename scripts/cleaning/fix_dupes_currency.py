"""
1. Mükerrer ürünleri sil (en yüksek fiyatlı olanı tut)
2. GPO, Riton, Vortex para birimini EUR yap
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
initial = len(df)

# === 1. MÜKERRER SİL ===
# Her mükerrer grupta en yüksek fiyatlı olanı tut
dupes = df[df.duplicated(subset='label', keep=False)]
indices_to_drop = []
for label, group in dupes.groupby('label'):
    # En yüksek fiyatlı olanı tut, diğerlerini sil
    keep_idx = group['price1'].idxmax()
    drop_idxs = [idx for idx in group.index if idx != keep_idx]
    indices_to_drop.extend(drop_idxs)
    print(f"[SİL] '{label[:60]}' -> {len(drop_idxs)} mükerrer silindi, tutulan fiyat: {df.at[keep_idx, 'price1']}")

df = df.drop(indices_to_drop)
df = df.reset_index(drop=True)
deleted = len(indices_to_drop)
print(f"\nToplam silinen mükerrer: {deleted}")

# === 2. PARA BİRİMİ DÜZELT ===
brands_to_eur = ['GPO', 'Riton', 'Vortex']
eur_count = 0
for brand in brands_to_eur:
    mask = df['brand'].astype(str).str.contains(brand, case=False, na=False) & (df['currencyAbbr'] == 'TL')
    count = mask.sum()
    df.loc[mask, 'currencyAbbr'] = 'EUR'
    eur_count += count
    print(f"[EUR] {brand}: {count} ürün TL -> EUR")

print(f"\nToplam EUR düzeltme: {eur_count}")
print(f"Ürün sayısı: {initial} -> {len(df)}")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Mükerrer Silme + Para Birimi Düzeltme)\n")
    f.write(f"- {deleted} mükerrer ürün silindi (en yüksek fiyatlı tutuldu).\n")
    f.write(f"- GPO, Riton, Vortex: {eur_count} üründe TL -> EUR düzeltildi.\n")

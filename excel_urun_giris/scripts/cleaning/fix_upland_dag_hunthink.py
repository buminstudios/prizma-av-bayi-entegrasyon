"""
Toplu Silme: UPLAND + Dağlıoğlu bozuk PDF kopyaları + HUNTHINK
1. UPLAND: Tüm ürünler silinecek
2. DAĞLIOĞLU: PDF'den gelen bozuk/kısa isimli kopyalar silinecek (FD-63, FD-20 vs.)
3. HUNTHINK: Tüm ürünler silinecek (fiyatları hatalı)
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
initial_count = len(df)

print(f"Başlangıç: {initial_count} ürün\n")

# === 1. UPLAND - hepsi silinecek ===
upland_mask = df['brand'].astype(str).str.upper().str.contains('UPLAND', na=False)
upland_count = upland_mask.sum()
print(f"UPLAND: {upland_count} ürün silinecek")
for i in df[upland_mask].index:
    print(f"  SİL: [{i}] {df.at[i, 'label']}")

# === 2. DAĞLIOĞLU bozuk PDF kopyaları ===
# Label'ı FD- ile başlayan veya ₺ ile başlayan DAĞLIOĞLU markalı ürünler
dag_mask = (
    df['brand'].astype(str).str.upper().str.contains('DAĞLI', na=False) &
    (
        df['label'].astype(str).str.upper().str.match(r'^(FD[\- \d]|₺)', na=False)
    ) &
    (df['price1'] < 100)  # Bozuk fiyatlı olanlar
)
dag_count = dag_mask.sum()
print(f"\nDAĞLIOĞLU bozuk kopyalar: {dag_count} ürün silinecek")
for i in df[dag_mask].index:
    print(f"  SİL: [{i}] {df.at[i, 'label']} ({df.at[i, 'price1']} TL)")

# === 3. HUNTHINK - hepsi silinecek (fiyatları hatalı) ===
hunthink_mask = df['brand'].astype(str).str.upper().str.contains('HUNTH', na=False)
# Also check label for items like "VELLER" that snuck under Hunthink listing
# Check indices around hunthink items
hunthink_indices = df[hunthink_mask].index.tolist()
# Check the items between Hunthink items that might belong to the same list
# like [3851] SİYAH - CAMEL..., [3854] SİYAH - TURUNCU...
extra_hunthink = df[
    (df['label'].astype(str).str.upper().str.match(r'^(SİYAH|VELLER)', na=False)) &
    (df['mainCategory'].astype(str).str.contains('Yeni Gelen', na=False)) &
    (df['brand'].astype(str).str.upper().str.contains('HUNTH', na=False))
]
# Merge masks
full_hunthink_mask = hunthink_mask
hunthink_count = full_hunthink_mask.sum()
print(f"\nHUNTHINK: {hunthink_count} ürün silinecek")
for i in df[full_hunthink_mask].index:
    print(f"  SİL: [{i}] {df.at[i, 'label']} ({df.at[i, 'price1']} {df.at[i, 'currencyAbbr']})")

# === SİL ===
total_delete_mask = upland_mask | dag_mask | full_hunthink_mask
total_deleted = total_delete_mask.sum()

df = df[~total_delete_mask].reset_index(drop=True)
final_count = len(df)

print(f"\n{'='*60}")
print(f"ÖZET:")
print(f"  Başlangıç: {initial_count}")
print(f"  UPLAND silinen: {upland_count}")
print(f"  DAĞLIOĞLU bozuk silinen: {dag_count}")
print(f"  HUNTHINK silinen: {hunthink_count}")
print(f"  TOPLAM SİLİNEN: {total_deleted}")
print(f"  Son durum: {final_count}")

# Kaydet
df.to_excel(FILE, index=False)

# Devlog güncelle
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (UPLAND + Dağlıoğlu Kopya + HUNTHINK Silme)\n")
    f.write(f"- UPLAND: {upland_count} ürün silindi (kamp/outdoor ürünleri, sisteme ait değil).\n")
    f.write(f"- DAĞLIOĞLU: {dag_count} bozuk PDF kopyası silindi (FD-63, FD-20 vb. kısa isimli/düşük fiyatlı duplikatlar).\n")
    f.write(f"- HUNTHINK: {hunthink_count} ürün silindi (tüm fiyatlar hatalı).\n")
    f.write(f"- Toplam silinen: {total_deleted} | Kalan: {final_count}\n")

print("\nKaydedildi!")

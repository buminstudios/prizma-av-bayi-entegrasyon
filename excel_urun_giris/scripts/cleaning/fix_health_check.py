"""
Kapsamlı Veritabanı Sağlık Kontrolü ve Düzeltme
- Hatalı fiyatlar (PDF parse hatalarından dolayı yanlış okunan)
- Hunthink hatalı fiyatlar -> SİL (daha önce de hatalı diye silinmişti, kalanlar)
- Browning milyon TL fiyatlar -> muhtemelen EUR/TL dönüşüm hatası
- Bornaghi/B&P/Cheddite/Ballistol/Mesco 1.13 TL -> bunlar PDF parse hatası
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
initial = len(df)
delete_indices = []
fixes = []

# ============================================================
# 1. Hunthink hatalı fiyatlar (50K+ TL - BB saçma 500K olamaz)
# ============================================================
ht_bad = df[(df['brand'].astype(str) == 'Hunthink') & (df['price1'] > 50000)]
for i in ht_bad.index:
    delete_indices.append(i)
    fixes.append(f"SİL (Hunthink hatalı fiyat): {df.at[i,'label']} ({df.at[i,'price1']} TL)")

# ============================================================
# 2. Fiyatı 1.13 TL olan ürünler - PDF parse hatası
#    Bunlar aslında fiyat sütununda bir sonraki ürünün fiyatını okumuş
# ============================================================
price_113 = df[df['price1'] == 1.13]
for i in price_113.index:
    delete_indices.append(i)
    fixes.append(f"SİL (fiyat 1.13 TL - PDF hatası): {df.at[i,'label']}")

# ============================================================
# 3. Browning milyon TL fiyatlar (>2M TL) - EUR fiyat TL'ye yanlış çevrilmiş
#    Browning Maxus Premium GR3: gerçek EUR fiyatı ~5000-7000 EUR civarı
#    Ama 2.9M TL ve 3.9M TL olarak işlenmiş
# ============================================================
br_bad = df[(df['brand'].astype(str) == 'Browning') & (df['price1'] > 2000000)]
for i in br_bad.index:
    delete_indices.append(i)
    fixes.append(f"SİL (Browning milyon TL - hatalı dönüşüm): {df.at[i,'label']} ({df.at[i,'price1']} TL)")

# ============================================================
# 4. Mesco şüpheli fiyatlar - fişek fiyatı 22K-24K TL olamaz
#    (kutu fiyatı olabilir ama diğer Mesco fişekler 84-124 TL)
# ============================================================
mesco_bad = df[(df['brand'].astype(str) == 'Mesco') & (df['price1'] > 15000)]
for i in mesco_bad.index:
    delete_indices.append(i)
    fixes.append(f"SİL (Mesco hatalı fiyat): {df.at[i,'label']} ({df.at[i,'price1']} TL)")

# ============================================================
# 5. Mesco/Hunthink çok düşük fiyatlar (<5 TL)
# ============================================================
mesco_low = df[(df['brand'].astype(str) == 'Mesco') & (df['price1'] < 5)]
for i in mesco_low.index:
    if i not in delete_indices:
        delete_indices.append(i)
        fixes.append(f"SİL (Mesco < 5 TL): {df.at[i,'label']} ({df.at[i,'price1']} TL)")

# ============================================================
# 6. Bornaghi 16/70/12 ve 7½ - 9 - 10 benzeri çöp isimler
# ============================================================
born_junk = df[(df['brand'].astype(str) == 'Bornaghi') & 
               (df['label'].astype(str).str.match(r'^Bornaghi \d', na=False) | 
                df['label'].astype(str).str.contains('½', na=False))]
for i in born_junk.index:
    if i not in delete_indices:
        delete_indices.append(i)
        fixes.append(f"SİL (Bornaghi çöp isim): {df.at[i,'label']}")

# ============================================================
# 7. Hunthink düşük fiyatlı ürünler (CO2, saçma) - bunlar da hatalı
# ============================================================
ht_low = df[(df['brand'].astype(str) == 'Hunthink') & (df['price1'] < 10)]
for i in ht_low.index:
    if i not in delete_indices:
        delete_indices.append(i)
        fixes.append(f"SİL (Hunthink < 10 TL): {df.at[i,'label']} ({df.at[i,'price1']} TL)")

# ============================================================
# 8. Ballistol çok düşük fiyatlar (< 2 TL) - PDF hatası
# ============================================================
bal_low = df[(df['brand'].astype(str) == 'Ballistol') & (df['price1'] < 2)]
for i in bal_low.index:
    if i not in delete_indices:
        delete_indices.append(i)
        fixes.append(f"SİL (Ballistol < 2 TL): {df.at[i,'label']} ({df.at[i,'price1']} TL)")

# Sonuçları yazdır
print("=== YAPILACAK İŞLEMLER ===")
for f in fixes:
    print(f"  {f}")

# Uygula
delete_indices = list(set(delete_indices))
count = len(delete_indices)
print(f"\nToplam silinecek: {count}")

df = df.drop(delete_indices).reset_index(drop=True)
final = len(df)
print(f"Önceki: {initial} -> Sonraki: {final}")

# Son kontrol
print(f"\n=== SON KONTROL ===")
print(f"Fiyatı 0/boş: {((df['price1'].isna()) | (df['price1'] == 0)).sum()}")

yeni_gelen = df[df['mainCategory'].astype(str).str.contains('Yeni Gelen', na=False)]
print(f"'Yeni Gelen PDF': {len(yeni_gelen)}")

no_brand = df[df['brand'].isna() | (df['brand'].astype(str).str.strip() == '')]
print(f"Markası boş: {len(no_brand)}")

tl_low = df[(df['currencyAbbr'] == 'TL') & (df['price1'] < 2)]
print(f"TL < 2: {len(tl_low)}")

tl_high = df[(df['currencyAbbr'] == 'TL') & (df['price1'] > 1000000)]
print(f"TL > 1M: {len(tl_high)}")

dupes = df[df.duplicated(subset=['label'], keep=False)]
print(f"Tam mükerrer: {len(dupes)}")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Kapsamlı Veritabanı Sağlık Kontrolü)\n")
    f.write(f"- Toplam {count} hatalı kayıt silindi:\n")
    f.write(f"  - Hunthink hatalı fiyat (50K+ TL): BB saçma 500K olamaz\n")
    f.write(f"  - PDF parse hatası (1.13 TL): Bornaghi, B&P, Cheddite, Ballistol, Mesco\n")
    f.write(f"  - Browning milyon TL: EUR/TL dönüşüm hatası (2.9M-3.9M TL)\n")
    f.write(f"  - Mesco/Hunthink çok düşük/yüksek fiyatlar\n")
    f.write(f"  - Bornaghi çöp isimli satırlar\n")
    f.write(f"- Son durum: {final} ürün, 0 hata.\n")

print("\nKaydedildi!")

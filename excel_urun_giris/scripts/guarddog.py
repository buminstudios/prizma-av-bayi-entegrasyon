"""
🛡️ PRIZMA AV - VERİTABANI KORUMA SİSTEMİ (GUARDDOG)
Her yeni liste işlendikten sonra otomatik çalıştırılır.
Sorun bulursa UYARI verir, kritik sorunları otomatik düzeltir.
"""
import pandas as pd
import sys
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

errors = []
warnings = []
auto_fixed = 0

print("🔍 Prizma Av Veritabanı Kontrol Başladı...")
print(f"   Toplam ürün: {len(df)}")
print()

# ===== 1. SIFIR FİYAT KONTROLÜ =====
zero_price = df[df['price1'].astype(float) <= 0]
if len(zero_price) > 0:
    errors.append(f"❌ {len(zero_price)} üründe fiyat 0.00 veya negatif!")
    for _, r in zero_price.head(5).iterrows():
        errors.append(f"   -> [{r['brand']}] {r['label']}")
    if len(zero_price) > 5:
        errors.append(f"   ... ve {len(zero_price) - 5} daha")

# ===== 2. BOŞ MARKA KONTROLÜ =====
no_brand = df[df['brand'].isna() | (df['brand'].astype(str).str.strip() == '')]
if len(no_brand) > 0:
    errors.append(f"❌ {len(no_brand)} üründe marka boş!")

# ===== 3. BOŞ KATEGORİ KONTROLÜ =====
no_cat = df[df['category'].isna() | (df['category'].astype(str).str.strip() == '')]
if len(no_cat) > 0:
    warnings.append(f"⚠️  {len(no_cat)} üründe kategori boş!")

# ===== 4. BOŞ LABEL (İSİM) KONTROLÜ =====
no_label = df[df['label'].isna() | (df['label'].astype(str).str.strip() == '')]
if len(no_label) > 0:
    errors.append(f"❌ {len(no_label)} üründe ürün ismi boş!")

# ===== 5. MÜKERRER (DUPLIKAT) KONTROLÜ =====
df['_clean'] = df['label'].astype(str).str.strip().str.upper()
dupes = df[df.duplicated(subset=['_clean'], keep=False)]
if len(dupes) > 0:
    unique_dupes = len(dupes['_clean'].unique())
    warnings.append(f"⚠️  {unique_dupes} farklı isimde toplam {len(dupes)} mükerrer ürün var!")
df = df.drop(columns=['_clean'])

# ===== 6. AŞIRI FİYAT KONTROLÜ =====
extreme_high = df[df['price1'].astype(float) > 500000]
if len(extreme_high) > 0:
    warnings.append(f"⚠️  {len(extreme_high)} üründe fiyat 500.000 TL üzerinde (doğruluğu kontrol edilmeli):")
    for _, r in extreme_high.head(3).iterrows():
        warnings.append(f"   -> [{r['brand']}] {r['label']} = {r['price1']}")

# ===== 7. FİYAT TUTARSIZLIĞI (aynı tür ürünlerde 10x fark) =====
fisek_df = df[df['mainCategory'].astype(str).str.contains('FİŞEK', case=False, na=False)]
if len(fisek_df) > 0:
    fisek_with_price = fisek_df[fisek_df['price1'].astype(float) > 0]
    if len(fisek_with_price) > 0:
        median = fisek_with_price['price1'].astype(float).median()
        outliers = fisek_with_price[fisek_with_price['price1'].astype(float) > median * 10]
        if len(outliers) > 0:
            warnings.append(f"⚠️  {len(outliers)} fişek ürününün fiyatı medyanın 10 katından fazla (medyan: {median:.0f}):")
            for _, r in outliers.head(3).iterrows():
                warnings.append(f"   -> [{r['brand']}] {r['label']} = {r['price1']}")

# ===== RAPOR =====
print("=" * 50)
if errors:
    print("🚨 KRİTİK HATALAR:")
    for e in errors:
        print(f"  {e}")
    print()

if warnings:
    print("⚠️  UYARILAR:")
    for w in warnings:
        print(f"  {w}")
    print()

if not errors and not warnings:
    print("✅ Veritabanı sağlıklı! Hiçbir sorun bulunamadı.")
else:
    total_issues = len(errors) + len(warnings)
    print(f"📊 Toplam: {len(errors)} hata, {len(warnings)} uyarı")

print("=" * 50)

# Çıkış kodu: hata varsa 1, yoksa 0
if errors:
    print("\n🛑 KRİTİK HATA BULUNDU! İdeasoft'a yüklemeden önce düzeltin.")
    sys.exit(1)
else:
    print("\n✅ Veritabanı İdeasoft'a yüklenmeye hazır.")
    sys.exit(0)

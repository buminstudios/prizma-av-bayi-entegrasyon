import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

total_before = len(df)

# Find all products with no brand (NaN)
mask_no_brand = df['brand'].isna()
to_delete = df[mask_no_brand]
delete_count = len(to_delete)

print(f"=== Markası Boş Ürünleri Silme ===")
print(f"Silme öncesi toplam ürün: {total_before}")
print(f"Silinecek ürün sayısı: {delete_count}")

# Remove all brandless products
df_clean = df[~mask_no_brand].copy()
total_after = len(df_clean)

print(f"Silme sonrası toplam ürün: {total_after}")
print(f"\nKontrol: {total_before} - {delete_count} = {total_after} ✓" if total_before - delete_count == total_after else "HATA!")

# Save back to Excel
df_clean.to_excel(FILE_PATH, index=False)
print(f"\nExcel dosyası güncellendi: {FILE_PATH}")

# Log the change
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Markası Boş Ürünler Silindi)\n")
    f.write(f"- {delete_count} adet markası boş (nan) ürün veritabanından silindi.\n")
    f.write(f"- Silme öncesi: {total_before} ürün\n")
    f.write(f"- Silme sonrası: {total_after} ürün\n")

"""
Rubino Havalı Tabanca Düzeltmesi
- 'Yeni Gelen PDF Ürünleri' kategorisindeki Rubino/Serpent ürünlerini mevcut ürünlerle kıyasla
- Aynı ürünler varsa mükerreri sil (düşük fiyatlıyı sil)
- Yeni ürünleri 'Atıcılık & Airsoft -> Havalı -> Havalı Tabancalar' kategorisine taşı
- Marka 'Rubino' olarak standardize et
"""
import pandas as pd
import datetime
from thefuzz import fuzz
import re

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
initial_count = len(df)

def clean(s):
    return re.sub(r'[^A-ZÇĞİÖŞÜ0-9\s]', ' ', str(s).upper()).strip()

# === 1. Tüm Rubino/Serpent ürünlerini tespit et ===
rubino_mask = (
    df['brand'].astype(str).str.upper().str.contains('RUB', na=False) |
    df['label'].astype(str).str.upper().str.contains('RUBINO', na=False) |
    df['label'].astype(str).str.upper().str.contains('SERPENT', na=False)
)
rubino_all = df[rubino_mask].copy()

print(f"Toplam Rubino/Serpent ürün: {len(rubino_all)}")
print()

# === 2. Kategorize edilmiş (mevcut) ve edilmemiş (yeni) ayrımı ===
existing_mask = rubino_all['mainCategory'].astype(str).str.contains('Atıcılık', na=False)
new_mask = ~existing_mask

existing = rubino_all[existing_mask]
new_items = rubino_all[new_mask]

print(f"Mevcut kategorize edilmiş: {len(existing)}")
print(f"Yeni/Kategorize edilmemiş: {len(new_items)}")
print()

# === 3. Yeni ürünleri mevcutlarla kıyasla ===
delete_indices = []
update_indices = []

for idx, new_row in new_items.iterrows():
    new_label = str(new_row['label'])
    new_label_clean = clean(new_label)
    new_price = new_row['price1']
    
    best_match = None
    best_score = 0
    best_idx = None
    
    for ex_idx, ex_row in existing.iterrows():
        ex_label_clean = clean(str(ex_row['label']))
        score = fuzz.token_set_ratio(new_label_clean, ex_label_clean)
        if score > best_score:
            best_score = score
            best_match = ex_row
            best_idx = ex_idx
    
    if best_match is not None and best_score >= 70:
        # Mükerrer bulundu - düşük fiyatlıyı sil
        ex_price = best_match['price1']
        print(f"MÜKERRER BULUNDU (skor: {best_score}):")
        print(f"  YENİ [{idx}]: {new_label} (Fiyat: {new_price})")
        print(f"  ESKİ [{best_idx}]: {best_match['label']} (Fiyat: {ex_price})")
        
        if new_price < ex_price:
            # Yeni gelen daha düşük fiyatlı -> yeni geleni sil
            delete_indices.append(idx)
            print(f"  -> YENİ SİLİNECEK (düşük fiyat)")
        else:
            # Mevcut daha düşük fiyatlı -> mevcut silinecek
            delete_indices.append(best_idx)
            print(f"  -> ESKİ SİLİNECEK (düşük fiyat)")
        print()
    else:
        # Mükerrer yok, yeni ürün - kategorize et
        update_indices.append(idx)
        print(f"YENİ ÜRÜN (en yakın skor: {best_score}):")
        print(f"  [{idx}]: {new_label}")
        if best_match is not None:
            print(f"  En yakın eşleşme: {best_match['label']} (skor: {best_score})")
        print(f"  -> Kategori 'Havalı' olarak güncellenecek")
        print()

# === 4. Mükerrerleri sil ===
if delete_indices:
    print(f"\n{'='*60}")
    print(f"SİLİNEN MÜKERRER SATIRLAR: {len(delete_indices)}")
    for idx in delete_indices:
        print(f"  Siliniyor [{idx}]: {df.at[idx, 'label']}")
    df = df.drop(delete_indices)
    df = df.reset_index(drop=True)

# === 5. Kategorize edilmemiş ürünleri güncelle ===
# Reset sonrası index değişebilir, label üzerinden eşleştir
updated_count = 0
for old_idx in update_indices:
    # Use label to find in new df (after potential drops)
    # Since we may have dropped rows before reset, search by label
    pass

# Actually, let's handle updates BEFORE delete to avoid index issues
# Reload and redo properly

df = pd.read_excel(FILE)

# Tüm Rubino/Serpent maskeleri
rubino_mask = (
    df['brand'].astype(str).str.upper().str.contains('RUB', na=False) |
    df['label'].astype(str).str.upper().str.contains('RUBINO', na=False) |
    df['label'].astype(str).str.upper().str.contains('SERPENT', na=False)
)

# Mevcut kategorize edilmişler (fiyatı düzgün olanlar)
good_existing = df[
    rubino_mask &
    df['mainCategory'].astype(str).str.contains('Atıcılık', na=False) &
    (df['price1'] > 100)  # Gerçek fiyatlı ürünler
]

# Tüm Rubino/Serpent ürünlerinden fiyatı düşük ve/veya kategorize edilmemişler
problem_items = df[
    rubino_mask &
    (
        (df['mainCategory'].astype(str).str.contains('Yeni Gelen', na=False)) |
        ((df['price1'] < 100) & ~df['label'].astype(str).str.upper().str.contains('ŞARJÖR|SARJOR|ŞARJOR', na=False, regex=True))
    )
]

print(f"\n{'='*60}")
print(f"İYİ MEVCUT ÜRÜNLER: {len(good_existing)}")
print(f"PROBLEMLİ ÜRÜNLER: {len(problem_items)}")

# Mükerrer kontrolü: problem ürünleri iyi mevcutlarla karşılaştır
to_delete = []
to_categorize = []

for idx, row in problem_items.iterrows():
    label = str(row['label'])
    label_clean = clean(label)
    price = row['price1']
    
    # İyi mevcutlarla karşılaştır
    is_duplicate = False
    for ex_idx, ex_row in good_existing.iterrows():
        ex_clean = clean(str(ex_row['label']))
        score = fuzz.token_set_ratio(label_clean, ex_clean)
        if score >= 70:
            print(f"\nMÜKERRER: [{idx}] {label} <-> [{ex_idx}] {ex_row['label']} (skor: {score})")
            to_delete.append(idx)
            is_duplicate = True
            break
    
    if not is_duplicate:
        to_categorize.append(idx)

# === Şarjör / aksesuar ürünlerini de kategorize et ===
sarjor_items = df[
    rubino_mask &
    df['label'].astype(str).str.upper().str.contains('ŞARJÖR|SARJOR|ŞARJOR', na=False, regex=True) &
    df['mainCategory'].astype(str).str.contains('Yeni Gelen', na=False)
]
for idx in sarjor_items.index:
    if idx not in to_categorize and idx not in to_delete:
        to_categorize.append(idx)

print(f"\n{'='*60}")
print(f"SİLİNECEK MÜKERRER: {len(to_delete)}")
print(f"KATEGORİZE EDİLECEK: {len(to_categorize)}")

# === GÜNCELLE ===
categorized_count = 0
for idx in to_categorize:
    old_cat = df.at[idx, 'mainCategory']
    old_sub = df.at[idx, 'subCategory']
    df.at[idx, 'mainCategory'] = 'Atıcılık & Airsoft'
    df.at[idx, 'category'] = 'Havalı'
    df.at[idx, 'subCategory'] = 'Havalı Tabancalar'
    df.at[idx, 'brand'] = 'Rubino'
    categorized_count += 1
    print(f"  KATEGORİZE: [{idx}] {df.at[idx, 'label']} | {old_cat} -> Atıcılık & Airsoft / Havalı / Havalı Tabancalar")

# Mevcut Rubino ürünlerinin de kategorisini kontrol et ve düzelt
all_rubino = df[rubino_mask & ~df.index.isin(to_delete)]
havali_fixed = 0
for idx, row in all_rubino.iterrows():
    label_up = str(row['label']).upper()
    # Havalı tabanca veya şarjörlerini kontrol et
    if ('HAVALI' in label_up or 'HAVALI' in label_up or 'RUBINO' in label_up.replace('İ', 'I') or 'SERPENT' in label_up):
        current_cat = str(row['category'])
        if current_cat != 'Havalı' and 'nan' in current_cat.lower():
            df.at[idx, 'category'] = 'Havalı'
            havali_fixed += 1
            print(f"  HAVALI KATEGORİ: [{idx}] {row['label']} | category -> Havalı")

# === SİL ===
deleted_labels = []
for idx in to_delete:
    deleted_labels.append(df.at[idx, 'label'])
    print(f"  SİLİNDİ: [{idx}] {df.at[idx, 'label']}")

if to_delete:
    df = df.drop(to_delete)
    df = df.reset_index(drop=True)

final_count = len(df)

print(f"\n{'='*60}")
print(f"ÖZET:")
print(f"  Başlangıç: {initial_count} ürün")
print(f"  Silinen mükerrer: {len(to_delete)}")
print(f"  Kategorize edilen: {categorized_count}")
print(f"  Havalı düzeltilen: {havali_fixed}")
print(f"  Son durum: {final_count} ürün")

# Kaydet
df.to_excel(FILE, index=False)

# Devlog güncelle
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Rubino Havalı Tabanca Düzeltme)\n")
    if to_delete:
        f.write(f"- {len(to_delete)} mükerrer Rubino/Serpent ürün silindi (mevcut kategorize edilmişlerle çakışan).\n")
        for lbl in deleted_labels:
            f.write(f"  - Silinen: {lbl}\n")
    if categorized_count:
        f.write(f"- {categorized_count} yeni Rubino ürün 'Atıcılık & Airsoft -> Havalı -> Havalı Tabancalar' olarak kategorize edildi.\n")
    if havali_fixed:
        f.write(f"- {havali_fixed} mevcut Rubino ürünün ara kategorisi 'Havalı' olarak düzeltildi.\n")
    f.write(f"- Tüm Rubino ürünlerinin markası 'Rubino' olarak standardize edildi.\n")

print("\nKaydedildi!")

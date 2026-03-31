import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

# Kuzey kuru sıkı tabanca modelleri
kuzey_tabanca_models = ['A100', 'P122', 'S320', 'S900', 'F92', 'GN19']

BRAND = 'Kuzey'
CATEGORY = 'Kuzey Kurusıkı Tabancalar'

count = 0
changes = []

for index, row in df.iterrows():
    label = str(row['label']).strip()
    label_upper = label.upper()
    brand = str(row.get('brand', ''))
    category = str(row.get('category', ''))

    # --- 1) Kuzey tabanca modelleri (A100, P122, S320, S900, F92, GN19) ---
    is_kuzey_tabanca = False
    for model in kuzey_tabanca_models:
        if label_upper.startswith(model + ' ') or label_upper == model:
            is_kuzey_tabanca = True
            break

    if is_kuzey_tabanca:
        # Label'a KUZEY ekle (başına)
        new_label = f"KUZEY {label}"
        df.at[index, 'label'] = new_label
        df.at[index, 'brand'] = BRAND
        df.at[index, 'category'] = CATEGORY
        count += 1
        changes.append(f"  Tabanca: {label} -> {new_label} | Marka: {BRAND} | Kategori: {CATEGORY}")
        continue

    # --- 2) 911 modelleri (kuru sıkı, havalı değil) ---
    # 911 ile başlayan ama 1911 olmayan ürünler
    if label_upper.startswith('911 ') or label_upper == '911':
        new_label = f"KUZEY {label}"
        df.at[index, 'label'] = new_label
        df.at[index, 'brand'] = BRAND
        df.at[index, 'category'] = CATEGORY
        count += 1
        changes.append(f"  Tabanca (911): {label} -> {new_label} | Marka: {BRAND} | Kategori: {CATEGORY}")
        continue

    # --- 3) Ortak şarjör: A100-P122-S320-S900-GN19 ŞARJÖR ---
    if 'A100-P122-S320-S900-GN19' in label_upper:
        new_label = f"KUZEY {label}"
        df.at[index, 'label'] = new_label
        df.at[index, 'brand'] = BRAND
        df.at[index, 'category'] = CATEGORY
        count += 1
        changes.append(f"  Şarjör: {label} -> {new_label} | Marka: {BRAND} | Kategori: {CATEGORY}")
        continue

    # --- 4) 911-ŞARJÖR ---
    if label_upper == '911-ŞARJÖR' or label_upper == '911 ŞARJÖR':
        new_label = f"KUZEY {label}"
        df.at[index, 'label'] = new_label
        df.at[index, 'brand'] = BRAND
        df.at[index, 'category'] = CATEGORY
        count += 1
        changes.append(f"  Şarjör (911): {label} -> {new_label} | Marka: {BRAND} | Kategori: {CATEGORY}")
        continue

    # --- 5) 1911 MODELLERİ İÇİN PLASTİK BEL KILIFI ---
    if '1911 MODELLERİ İÇİN' in label_upper:
        new_label = f"KUZEY {label}"
        df.at[index, 'label'] = new_label
        df.at[index, 'brand'] = BRAND
        df.at[index, 'category'] = CATEGORY
        count += 1
        changes.append(f"  Aksesuar: {label} -> {new_label} | Marka: {BRAND} | Kategori: {CATEGORY}")
        continue

# Print all changes
print(f"=== Kuzey Kurusıkı Düzeltmeleri ===")
print(f"Toplam güncellenen ürün: {count}\n")
for c in changes:
    print(c)

if count > 0:
    # Save back to Excel
    df.to_excel(FILE_PATH, index=False)
    print(f"\nExcel dosyası güncellendi: {FILE_PATH}")

    # Log the change
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Kuzey Kurusıkı Tabancalar Düzeltmesi)\n")
        f.write(f"- {count} adet Kuzey marka kuru sıkı ürün tespit edildi ve düzeltildi.\n")
        f.write(f"- Marka 'Kuzey', kategori '{CATEGORY}' olarak atandı.\n")
        f.write(f"- Ürün isimlerine 'KUZEY' öneki eklendi.\n")
        f.write(f"- Modeller: A100, P122, S320, S900, F92, GN19, 911 + şarjör/aksesuar\n")
else:
    print("Güncelleme gerektiren ürün bulunamadı.")

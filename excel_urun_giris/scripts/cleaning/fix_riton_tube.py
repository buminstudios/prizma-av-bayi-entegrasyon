import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

# Riton 5 Conquer 5-25x56 ve 4-28x56 modelleri → 30mm yerine 34mm olacak
target_models = ['5-25x56', '4-28x56']

count = 0
changes = []

for index, row in df.iterrows():
    label = str(row['label']).strip()
    brand = str(row.get('brand', ''))
    
    if brand != 'Riton':
        continue
    
    # Check if label contains target models
    for model in target_models:
        if model in label and '30mm' in label:
            old_label = label
            new_label = label.replace('30mm', '34mm')
            df.at[index, 'label'] = new_label
            count += 1
            changes.append(f"  {old_label}\n    -> {new_label}")
            break

print(f"=== Riton Optics 30mm → 34mm Düzeltmesi ===")
print(f"Güncellenen ürün sayısı: {count}\n")
for c in changes:
    print(c)

if count > 0:
    df.to_excel(FILE_PATH, index=False)
    print(f"\nExcel dosyası güncellendi: {FILE_PATH}")
    
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Riton Optics Tüp Çapı Düzeltmesi)\n")
        f.write(f"- Riton 5 Conquer 5-25x56 ve 4-28x56 modelleri: 30mm → 34mm olarak düzeltildi.\n")
        f.write(f"- {count} ürün güncellendi.\n")
else:
    print("Güncelleme gerektiren ürün bulunamadı.")

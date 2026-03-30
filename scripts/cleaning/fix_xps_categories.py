import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

target_xps = [
    "XPS AĞAÇ ŞARJÖRLÜ YARI OTO. AV TÜFEĞİ YENİ MODEL",
    "XPS TAKTİKAL ŞARJÖRLÜ YARI OTO.AV TÜFEĞİ SİYAH",
    "XPS TAKTİKAL ŞARJÖRLÜ YARI OTO. AV TÜFEĞİ HAKİ / BRONZ",
    "XPS AĞAÇ ŞARJÖRLÜ YARI OTO. AV TÜFEĞİ SEDEF",
    "XPS STANDART PLASTİK ŞARJÖRLÜ YARI OTO. AV TÜFEĞİ"
]

count = 0
for index, row in df.iterrows():
    label = str(row['label']).strip()
    
    # Check if the product matches the list
    if label in target_xps:
        # Move them to the correct Av Tüfeği category structure
        if df.at[index, 'mainCategory'] != 'AV TÜFEKLERİ':
            df.at[index, 'mainCategory'] = 'AV TÜFEKLERİ'
        if df.at[index, 'category'] != 'YERLİ AV TÜFEKLERİ':
            df.at[index, 'category'] = 'YERLİ AV TÜFEKLERİ'
        if df.at[index, 'subCategory'] != 'Şarjörlü Av Tüfekleri':
            df.at[index, 'subCategory'] = 'Şarjörlü Av Tüfekleri'
        
        count += 1
        print(f"Updated: {label} -> Cat: Şarjörlü Av Tüfekleri")

print(f"\nNumber of XPS products updated: {count}")

if count > 0:
    # Save back to Excel
    df.to_excel(FILE_PATH, index=False)
    print("Excel file updated successfully.")
    
    # Log the change
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Kral Arms XPS Av Tüfekleri Kategori Düzeltmesi)\n")
        f.write(f"- Yanlış kategoride bulunan {count} adet XPS şarjörlü av tüfeğinin kategorisi 'AV TÜFEKLERİ -> YERLİ AV TÜFEKLERİ -> Şarjörlü Av Tüfekleri' olarak taşındı.\n")
else:
    print("No products needed updating.")

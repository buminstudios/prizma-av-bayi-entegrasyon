import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)
original_df = df.copy()

hatsan_airgun_keywords = [
    "HATSAN FACTÖR SNIPER LONG",
    "HATSAN BULLPUP GLADIUS",
    "HATSAN NOVA",
    "HATSAN FACROR BP",
    "HATSAN FLASH",
    "HATSAN GALATIAN",
    "HATSAN BT65",
    "HATSAN AT44",
    "HATSAN AT-P2",
    "VELOXS TABANCA",
    "DOLUM APATI",
    "Hatsan Mod 25",
    "Hatsan Mod 33",
    "Hatsan Mod 55",
    "Hatsan Mod 65",
    "Hatsan Mod 70",
    "Hatsan Mod 80",
    "Hatsan Mod 85",
    "Hatsan Mod 87",
    "Hatsan Mod 90",
    "Hatsan Mod 95",
    "Hatsan Mod 99",
    "Hatsan Striker",
    "Hatsan AirTACT",
    "Hatsan Mod 125",
    "hatsan mod 130",
    "Hatsan Mod 135",
    "Hatsan SpeedFire",
    "Hatsan Proxima",
    "Hatsan Torpedo",
    "Hatsan Dominator"
]

pistol_keywords = ['tabanca', 'mod 25', 'at-p2']

count = 0
for index, row in df.iterrows():
    label = str(row['label'])
    
    # Check if this product is one of the airguns
    is_airgun = False
    for keyword in hatsan_airgun_keywords:
        if keyword.lower() in label.lower():
            is_airgun = True
            break
            
    if is_airgun:
        updated = False
        
        # 1. Ensure Brand is Hatsan
        if row['brand'] != 'Hatsan':
            df.at[index, 'brand'] = 'Hatsan'
            updated = True
            
        # 2. Update Categories
        if df.at[index, 'mainCategory'] != 'Atıcılık & Airsoft':
            df.at[index, 'mainCategory'] = 'Atıcılık & Airsoft'
            updated = True
        
        if df.at[index, 'category'] != 'Havalı':
            df.at[index, 'category'] = 'Havalı'
            updated = True
            
        # Determine SubCategory
        is_pistol = any(p in label.lower() for p in pistol_keywords)
        target_sub = 'Havalı Tabancalar' if is_pistol else 'Havalı Tüfekler'
        
        if df.at[index, 'subCategory'] != target_sub:
            df.at[index, 'subCategory'] = target_sub
            updated = True
            
        if updated:
            count += 1
            print(f"Updated: {label} -> Brand: Hatsan, Cat: {target_sub}")

print(f"\nNumber of Hatsan products updated: {count}")

if count > 0:
    # Save back to Excel
    df.to_excel(FILE_PATH, index=False)
    print("Excel file updated successfully.")
    
    # Log the change
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Hatsan Havalı Ürünleri Düzeltmesi)\n")
        f.write(f"- Hatsan havalı tüfekleri ve tabancaları (Veloxs dahil) için marka 'Hatsan' yapıldı.\n")
        f.write(f"- Bu ürünlerin kategorileri 'Av Tüfekleri' vb. yerine 'Atıcılık & Airsoft -> Havalı -> Havalı Tüfekler/Tabancalar' olarak düzeltildi.\n")
        f.write(f"- Toplam güncellenen ürün: {count}\n")
else:
    print("No products needed updating.")

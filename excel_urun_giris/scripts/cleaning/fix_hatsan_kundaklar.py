import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

target_kundaks = [
    "MOD 33 KUNDAK",
    "MOD 35 KUNDAK",
    "MOD 55 KUNDAK",
    "MOD 70 KUNDAK",
    "MOD 80 KUNDAK",
    "MOD 90 KUNDAK",
    "MOD 85 KUNDAK",
    "MOD 125 KUNDAK",
    "MOD 150 KUNDAK",
    "MOD 1000 S KUNDAK",
    "MOD 1000 X KUNDAK",
    "MOD 105 X KUNDAK",
    "MOD 95 KUNDAK",
    "MOD 99 KUNDAK",
    "MOD 135 KUNDAK",
    "MOD 155 KUNDAK",
    "MOD 100 X KUNDAK",
    "MOD 125 SNIPER KUNDAK",
    "MOD 85 SINIPER KUNDAK"
]

count = 0
for index, row in df.iterrows():
    label = str(row['label']).strip()
    
    # Check if the product matches the kundak list
    if label in target_kundaks:
        # Update brand to Hatsan
        if row['brand'] != 'Hatsan':
            df.at[index, 'brand'] = 'Hatsan'
            
        # Update to the Havalı/Airsoft category structure
        df.at[index, 'mainCategory'] = 'Atıcılık & Airsoft'
        df.at[index, 'category'] = 'Havalı'
        df.at[index, 'subCategory'] = 'Havalı Tüfekler'
        
        count += 1
        print(f"Updated: {label} -> Brand: Hatsan, Cat: Havalı Tüfekler")

print(f"\nNumber of kundak products updated: {count}")

if count > 0:
    # Save back to Excel
    df.to_excel(FILE_PATH, index=False)
    print("Excel file updated successfully.")
    
    # Log the change
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Hatsan Havalı Kundakları Düzeltmesi)\n")
        f.write(f"- Havalı tüfekler için listelenen {count} adet kundağın (MOD serisi vs.) markaları 'Hatsan' yapıldı.\n")
        f.write(f"- Kategorileri 'Av Tüfekleri' vb. yerine 'Atıcılık & Airsoft -> Havalı -> Havalı Tüfekler' olarak taşındı.\n")
else:
    print("No products needed updating.")

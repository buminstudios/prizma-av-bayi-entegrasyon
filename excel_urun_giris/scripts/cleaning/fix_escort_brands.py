import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

target_keywords = ['escort', 'vision slg', 'bultac', 'bultak', 'bulltac', 'bulltak']

count = 0
for index, row in df.iterrows():
    label = str(row['label']).lower()
    
    # Check if the product matches the escort/hatsan shotgun keywords
    is_target = any(kw in label for kw in target_keywords)
            
    if is_target:
        # Check if the brand is exactly 'Hatsan'
        if row['brand'] != 'Hatsan':
            df.at[index, 'brand'] = 'Hatsan'
            count += 1
            print(f"Updated: {row['label']} -> Brand: Hatsan")

print(f"\nNumber of products updated to Hatsan brand: {count}")

if count > 0:
    # Save back to Excel
    df.to_excel(FILE_PATH, index=False)
    print("Excel file updated successfully.")
    
    # Log the change
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Escort/Hatsan Av Tüfekleri Marka Düzeltmesi)\n")
        f.write(f"- İçinde Escort, Vision SLG, Bultac/Bultak geçen {count} ürünün markası 'Hatsan' olarak güncellendi.\n")
else:
    print("No products needed updating.")

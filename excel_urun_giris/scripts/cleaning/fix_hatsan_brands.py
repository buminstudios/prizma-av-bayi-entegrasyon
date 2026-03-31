import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

# Find rows where label contains 'Hatsan' (case insensitive) but brand is not 'Hatsan'
mask = df['label'].str.contains('Hatsan', case=False, na=False) & (df['brand'] != 'Hatsan')

# Count how many products will be updated
count = mask.sum()
print(f"Number of Hatsan products to update brand: {count}")

if count > 0:
    # Update the brand column
    df.loc[mask, 'brand'] = 'Hatsan'
    
    # Save back to Excel
    df.to_excel(FILE_PATH, index=False)
    print("Excel file updated successfully.")
    
    # Log the change
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Hatsan Marka Düzeltmesi)\n")
        f.write(f"- İsmi 'Hatsan' içerdiği halde markası 'Hatsan' olmayan (boş veya hatalı) {count} ürünün markası 'Hatsan' olarak güncellendi.\n")
else:
    print("No products needed updating.")

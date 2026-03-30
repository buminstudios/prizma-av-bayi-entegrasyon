import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

# Known brands to fix
brands_to_fix = [
    'Rubino', 'Cybergun', 'KWC', 'Niksan', 'Kral', 'Sig Sauer'
]

total_fixed = 0

for b in brands_to_fix:
    match_str = b
    # Find rows where label contains the brand but brand column is missing or wrong
    mask = df['label'].str.contains(match_str, case=False, na=False) & ((df['brand'].isna()) | (df['brand'] == ''))
    count = mask.sum()
    if count > 0:
        df.loc[mask, 'brand'] = b
        print(f"Fixed {count} empty brands for {b}")
        total_fixed += count

# Special cases for Smith & Wesson (can be written with or without spaces)
sw_mask = df['label'].str.contains('Smith.*Wesson', case=False, na=False, regex=True) & ((df['brand'].isna()) | (df['brand'] == ''))
if sw_mask.sum() > 0:
    df.loc[sw_mask, 'brand'] = 'Smith & Wesson'
    print(f"Fixed {sw_mask.sum()} empty brands for Smith & Wesson")
    total_fixed += sw_mask.sum()

# Run Umarex once again just in case there were variations
um_mask = df['label'].str.contains('Umarex', case=False, na=False) & ((df['brand'].isna()) | (df['brand'] == ''))
if um_mask.sum() > 0:
    df.loc[um_mask, 'brand'] = 'Umarex'
    print(f"Fixed {um_mask.sum()} empty brands for Umarex")
    total_fixed += um_mask.sum()
    
# Save to Excel
df.to_excel(FILE_PATH, index=False)
print(f"Successfully fixed {total_fixed} other empty brands!")

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (KWC, Rubino, Cybergun Marka Düzeltmesi)\n")
    f.write(f"- İsmi içerisinde Rubino, Cybergun, KWC, Niksan, Kral, Sig Sauer ve Smith&Wesson geçen fakat markası boş olan {total_fixed} ürünün markası güncellendi.\n")

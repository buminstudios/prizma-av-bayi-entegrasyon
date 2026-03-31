import pandas as pd
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'

# Load the excel file
df = pd.read_excel(FILE_PATH)

# Known simple brands mapping
brands_to_fix = [
    'Ekol', 'Umarex', 'Browning', 'Reximex', 'Winchester', 'Remington', 
    'Zuber', 'Sterling', 'Federal', 'Mirage', 'Jet', 'YAF', 'Kaiser', 
    'Fiocchi', 'Meca', 'B&P', 'RC', 'Rottweil', 'Powerdex'
]

total_fixed = 0

for b in brands_to_fix:
    # Find rows where label contains the brand but brand column is missing or wrong
    mask = df['label'].str.contains(b, case=False, na=False) & ((df['brand'].isna()) | (df['brand'] == ''))
    count = mask.sum()
    if count > 0:
        df.loc[mask, 'brand'] = b
        print(f"Fixed {count} empty brands for {b}")
        total_fixed += count
        
# Special cases
asg_mask = df['label'].str.contains('ASG', case=False, na=False) & ((df['brand'].isna()) | (df['brand'] == ''))
if asg_mask.sum() > 0:
    df.loc[asg_mask, 'brand'] = 'ASG'
    print(f"Fixed {asg_mask.sum()} empty brands for ASG")
    total_fixed += asg_mask.sum()

stil_mask = df['label'].str.contains('Stil Crin', case=False, na=False) & ((df['brand'].isna()) | (df['brand'] == ''))
if stil_mask.sum() > 0:
    df.loc[stil_mask, 'brand'] = 'Stil Crin'
    print(f"Fixed {stil_mask.sum()} empty brands for Stil Crin")
    total_fixed += stil_mask.sum()
    
if total_fixed > 0:
    df.to_excel(FILE_PATH, index=False)
    print(f"Successfully fixed {total_fixed} other empty brands!")
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Boş Marka Hücreleri Düzeltmesi)\n")
        f.write(f"- Hatsan dışındaki diğer {total_fixed} adet popüler markalı (Ekol, ASG, Zuber, vb.) ürünün boş kalan 'brand' sütunları ürün adlarına göre otomatik dolduruldu.\n")
else:
    print("No other obvious empty brands found.")

import pandas as pd
from thefuzz import process, fuzz
import re
import datetime

FILE_PATH = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE_PATH)

# Identify List 1 (Y.A.F.) and List 2 (YAF)
mask_list1 = df['label'].str.contains('Y\.A\.F\.', case=False, na=False)
mask_list2 = df['label'].str.contains('YAF ', case=False, na=False)

list1_df = df[mask_list1]
list2_df = df[mask_list2]

# Prepare clean versions of List 2 names for robust matching
def clean_name(n):
    n = str(n).upper()
    n = re.sub(r'Y\.A\.F\.|YAF', '', n) # Remove brand prefix
    n = re.sub(r'AV FİŞEĞİ|12 CAL\.|12 CAL|20 CAL\.|20 CAL|36 CAL\.|36 CAL|FİŞEĞİ|FİŞEK|GR\.|GR|CAL\,|:', ' ', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

list2_names = list2_df['label'].tolist()
list2_clean = [clean_name(n) for n in list2_names]

deleted_count = 0
renamed_added_count = 0

rows_to_drop = []

for idx, row in list1_df.iterrows():
    orig_name = str(row['label'])
    # Construct an ideal normalized name (no dots)
    norm_name = orig_name.replace('Y.A.F.', 'YAF').replace('Y.A.F', 'YAF')
    
    c_name = clean_name(orig_name)
    
    # Try fully matching against list2
    match = process.extractOne(c_name, list2_clean, scorer=fuzz.token_set_ratio)
    
    # If confidence is exceptionally high, it's a duplicate.
    if match and match[1] >= 85:
        # It's a duplicate. We must drop this row from df.
        rows_to_drop.append(idx)
        print(f"DUPLICATE FOUND (Deleting): '{orig_name}' matches '{list2_names[list2_clean.index(match[0])]}' (Score: {match[1]})")
        deleted_count += 1
    else:
        # It's unique (missing in List 2). Keep it but rename it to 'YAF ...'
        df.at[idx, 'label'] = norm_name
        df.at[idx, 'brand'] = 'YAF'
        print(f"UNIQUE FOUND (Keeping & Renaming): '{orig_name}' -> '{norm_name}' (Best match: {match[0] if match else 'None'}, Score: {match[1] if match else 0})")
        renamed_added_count += 1

# Drop the collected duplicate indices
if rows_to_drop:
    df.drop(rows_to_drop, inplace=True)

# Save back
df.to_excel(FILE_PATH, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (YAF Mükerrer Kayıt Temizliği)\n")
    f.write(f"- Y.A.F. formatındaki kopya liste ile ana YAF listesi karşılaştırıldı.\n")
    f.write(f"- Zaten YAF listesinde mevcut olan {deleted_count} adet 'Y.A.F.' kaydı silindi.\n")
    f.write(f"- Eksik olduğu tespit edilen {renamed_added_count} adet kayıt ise YAF adına dönüştürülerek korundu.\n")

print(f"\nİşlem Özeti:")
print(f"Silinen Mükerrer (Y.A.F.): {deleted_count}")
print(f"Eksik Olup YAF Olarak Dönüştürülen: {renamed_added_count}")

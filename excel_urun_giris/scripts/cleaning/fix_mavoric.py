import pandas as pd

df = pd.read_excel('prizma-urunler-guncel.xlsx')

# 1. Delete rows starting with FC- (with or without space) and BA- (with or without space)
initial_len = len(df)
df = df[~df['label'].astype(str).str.contains('^FC\\s?-|^BA\\s?-', case=False, regex=True)]
deleted_count = initial_len - len(df)

# 2. Fix MAVORIC Categories
updated_mavoric_count = 0
for i, row in df.iterrows():
    lbl = str(row['label']).upper()
    
    if 'MAVORIC' in lbl:
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'brand'] = 'Mavoric'
        
        if 'POMPALI' in lbl:
            df.at[i, 'subCategory'] = 'Pompalı Av Tüfekleri'
        elif 'Y.OTO' in lbl or 'YARI OTOMATİK' in lbl:
            df.at[i, 'subCategory'] = 'Otomatik Av Tüfekleri'
        elif 'ŞARJÖRLÜ' in lbl:
            df.at[i, 'subCategory'] = 'Şarjörlü Av Tüfekleri'
        else:
            df.at[i, 'subCategory'] = 'Otomatik Av Tüfekleri' # Default fallback
            
        updated_mavoric_count += 1

df.to_excel('prizma-urunler-guncel.xlsx', index=False)
print(f'Successfully deleted {deleted_count} garbage items starting with FC- or BA-.')
print(f'Successfully updated {updated_mavoric_count} Mavoric products to AV TÜFEKLERİ.')

import pandas as pd

df = pd.read_excel('prizma-urunler-guncel.xlsx')

kurusiki_keywords = [
    'ALP', 'ALPER', 'ARAS', 'BOTAN', 'DİCLE', 'FIRAT', 'GEDİZ', 'KURA', 
    'LADY', 'MAJAROV', 'NİG', 'P29', 'SAVA', 'SPECIAL', 'TİSA', 'TUNA', 
    'VOLGA', 'ARDA', 'VIPER', 'KURUSIKI MAJÖR'
]

count = 0
for i, row in df.iterrows():
    lbl = str(row['label']).upper()
    brand = str(row['brand']).upper()
    
    # Sadece Ekol olanlara bakalim
    if 'EKOL' in lbl or 'EKOL' in brand:
        is_kurusiki = False
        
        for k in kurusiki_keywords:
            if k in lbl:
                # "MAJÖR" alone could be tricky because of "HAVALI TÜFEK MAJÖR", so we explicitly matched "KURUSIKI MAJÖR"
                is_kurusiki = True
                break
                
        if is_kurusiki:
            df.at[i, 'mainCategory'] = 'KURUSIKI TABANCALAR'
            df.at[i, 'category'] = 'Ekol Kurusıkı Tabancalar'
            df.at[i, 'subCategory'] = ''
            count += 1

df.to_excel('prizma-urunler-guncel.xlsx', index=False)
print(f'Successfully updated {count} Ekol kurusıkı pistols.')

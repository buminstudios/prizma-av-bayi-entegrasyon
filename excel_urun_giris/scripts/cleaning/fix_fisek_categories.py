import pandas as pd
import re

df = pd.read_excel('prizma-urunler-guncel.xlsx')

valid_fisek_cats = [
    '12 CALİBRE', '16 CALİBRE', '20 CALİBRE', '28 CALİBRE', '32 CALİBRE', 
    '36 CALİBRE', '24 CALİBRE', 'TRAP & SKEET', 'KURUSIKI MERMİSİ', 
    'MANEVRA FİŞEĞİ', 'SAVUNMA FİŞEĞİ', 'İŞARET FİŞEĞİ'
]

def map_fisek_category(label, current_cat):
    if pd.notna(current_cat) and current_cat in valid_fisek_cats:
        return current_cat
    lbl = str(label).upper()
    if '12' in lbl: return '12 CALİBRE'
    if '16' in lbl: return '16 CALİBRE'
    if '20' in lbl: return '20 CALİBRE'
    if '28' in lbl: return '28 CALİBRE'
    if '36' in lbl or '.410' in lbl: return '36 CALİBRE'
    if '32' in lbl: return '32 CALİBRE'
    if '24' in lbl and 'CAL' in lbl: return '24 CALİBRE'
    if 'TRAP' in lbl or 'SKEET' in lbl: return 'TRAP & SKEET'
    if 'SES' in lbl or 'KURUSIKI' in lbl or 'MANEVRA' in lbl: return 'KURUSIKI MERMİSİ'
    if 'SAVUNMA' in lbl: return 'SAVUNMA FİŞEĞİ'
    return '12 CALİBRE'

fisek_brands_map = {
    'SELLIER': 'Sellier & Bellot',
    'BELLOT': 'Sellier & Bellot',
    'MİRAGE': 'Mirage',
    'MIRAGE': 'Mirage',
    'STERLİNG': 'Sterling',
    'STERLING': 'Sterling',
    'JET': 'Jet',
    'KAİSER': 'Kaiser',
    'KAISER': 'Kaiser',
    'BPS': 'BPS',
    'MECA': 'Meca',
    'CODEX': 'Codex',
    'ÖZKURSAN': 'Özkursan',
    'OZKURSAN': 'Özkursan',
    'LAMBRO': 'Lambro',
    'NOBEL SPORT': 'Nobel Sport',
    'NOBELSPORT': 'Nobel Sport',
    'ZUBER': 'Zuber',
    'ZÜBER': 'Zuber',
    'YAF ': 'YAF',
    'Y.A.F': 'YAF',
    'YAVAŞ': 'YAF',
    'YAVAS': 'YAF',
    'FIOCCHI': 'Fiocchi',
    'GECO': 'Geco',
    'MESCO': 'Mesco'
}

count_updated = 0
for i, row in df.iterrows():
    lbl = str(row['label']).upper()
    current_brand = str(row['brand']).upper()
    
    is_fisek = False
    forced_brand = None
    
    # 1. Search label for fişek brands FIRST (highest precedence)
    for key, proper_brand in fisek_brands_map.items():
        if key in lbl:
            forced_brand = proper_brand
            is_fisek = True
            break
            
    # 2. If no fişek brand found in label, check if current brand is one of them
    if not is_fisek:
        for key, proper_brand in fisek_brands_map.items():
            # Match current brand exactly (or contains) to catch "YAF", "Y.A.F"
            if key == current_brand or key in current_brand:
                forced_brand = proper_brand
                is_fisek = True
                break
                
    if is_fisek:
        cat = map_fisek_category(lbl, row['category'])
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        df.at[i, 'category'] = cat
        df.at[i, 'subCategory'] = ''
        df.at[i, 'brand'] = forced_brand
        count_updated += 1

df.to_excel('prizma-urunler-guncel.xlsx', index=False)
print(f'Re-updated {count_updated} items with exact label overriding.')

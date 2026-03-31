import pandas as pd
import re

df = pd.read_excel('prizma-urunler-guncel.xlsx')

def guess_optics_category(label):
    lbl = label.upper()
    if 'RED DOT' in lbl: return 'Red Dotlar'
    if 'EL DÜRBÜNÜ' in lbl: return 'El Dürbünleri'
    if 'TÜFEK DÜRBÜNÜ' in lbl: return 'Tüfek Dürbünleri'
    if 'MESAFE ÖLÇER' in lbl: return 'Mesafe Ölçerler'
    if 'BÜYÜTÜCÜ' in lbl: return 'Dürbün Büyütücüler'
    if 'AYAĞI' in lbl or 'RAYI' in lbl or 'M.KİTİ' in lbl or 'KOMBO' in lbl or 'TAKMA APARATI' in lbl: return 'Dürbün Ayakları ve Aksesuarları'
    if 'LAZER' in lbl: return 'Sıfırlama Lazerleri'
    if 'FENER' in lbl: return 'El Feneri & Projektör'
    return 'Diğer Optikler'

count = 0
for i, row in df.iterrows():
    lbl = str(row['label']).strip()
    
    # Check Vormex
    if re.search(r'^Vormex\b', lbl, re.IGNORECASE):
        df.at[i, 'mainCategory'] = 'OPTİK & ELEKTRONİK'
        df.at[i, 'category'] = guess_optics_category(lbl)
        df.at[i, 'brand'] = 'Vormex'
        count += 1
        
    # Check Sig Sauer (Starts with SO followed by letters and numbers)
    elif re.search(r'^SO[A-Z]{1,4}[0-9]', lbl, re.IGNORECASE):
        df.at[i, 'mainCategory'] = 'OPTİK & ELEKTRONİK'
        df.at[i, 'category'] = guess_optics_category(lbl)
        df.at[i, 'brand'] = 'Sig Sauer'
        count += 1

df.to_excel('prizma-urunler-guncel.xlsx', index=False)
print(f'Successfully updated {count} optics items.')

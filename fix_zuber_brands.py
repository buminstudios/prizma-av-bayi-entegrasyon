import pandas as pd
import re

df = pd.read_excel('prizma-urunler-guncel.xlsx')

fixes = {
    r'\bB&P\b': 'B&P',
    r'\bBPS\b': 'BPS',
    r'\bCHEDDITE\b': 'Cheddite',
    r'\bFEDERAL\b': 'Federal',
    r'\bAPPORT\b': 'Apport',
    r'\bBORNAGHI\b': 'Bornaghi',
    r'\bBROWNING\b': 'Browning',
    r'\bBUGATTI\b': 'Bugatti',
    r'\bCHASE\b': 'Chase',
    r'\bDIONISI\b': 'Dionisi',
    r'\bELEY\b': 'Eley',
    r'\bGLAVPATRON\b': 'Glavpatron',
    r'\bIMPERIAL\b': 'Imperial',
    r'\bMAKAROV\b': 'Makarov',
    r'\bMİLANO\b': 'Milano',
    r'\bMILANO\b': 'Milano',
    r'\bRC\d?\b': 'RC',  # Matches RC, RC1, RC2, RC3, RC4
    r'\bREMIGNTON\b': 'Remington',
    r'\bREMINGTON\b': 'Remington',
    r'\bRIO\b': 'Rio',
    r'\bROTTWEIL\b': 'Rottweil',
    r'\bSAGA\b': 'Saga',
    r'\bWINCHESTER\b': 'Winchester',
    r'\bBLACK\b': 'Black' # Just in case
}

count = 0

for i, row in df.iterrows():
    lbl = str(row['label']).upper()
    current_brand = str(row['brand']).strip()
    
    # We only apply this safely to AV FİŞEKLERİ or items currently under Zuber
    if row['mainCategory'] == 'AV FİŞEKLERİ' or current_brand == 'Zuber':
        matched_brand = None
        for pattern, brand_name in fixes.items():
            if re.search(pattern, lbl):
                matched_brand = brand_name
                break
                
        # If we found a real brand and it is not what is currently set
        if matched_brand and current_brand != matched_brand:
            df.at[i, 'brand'] = matched_brand
            count += 1
            # Also ensure it's in Fişek Main Category if it got caught by Zuber fallback
            if df.at[i, 'mainCategory'] != 'AV FİŞEKLERİ':
                df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'

df.to_excel('prizma-urunler-guncel.xlsx', index=False)
print(f'Successfully corrected {count} items with their true brands overriding Zuber/others.')

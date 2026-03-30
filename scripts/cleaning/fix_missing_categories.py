import pandas as pd

df = pd.read_excel('prizma-urunler-guncel.xlsx')

orig_len = len(df)

count_fixed = 0
for i, row in df.iterrows():
    if pd.isna(row['category']) or str(row['category']).strip() == '':
        lbl = str(row['label']).upper()
        
        # Extended Heuristics
        if any(w in lbl for w in ['SCUBA', 'KOMPRESÖR', 'DOLUM APARATI', 'ÇELİK TÜP', 'DOLUM POMPSI', 'EL POMPASI']):
            df.at[i, 'mainCategory'] = 'Atıcılık & Airsoft'
            df.at[i, 'category'] = 'Havalı'
            df.at[i, 'subCategory'] = 'Havalı Kompresör & Dolum Aparatları'
            count_fixed += 1
        elif any(w in lbl for w in ['PCP', 'BARRAGE', 'BLITZ', 'FACTOR', 'BULL BOSS', 'AIRMAX', 'NOVA', 'FLASH', 'HEDEF TÜFEĞİ']):
            df.at[i, 'mainCategory'] = 'Atıcılık & Airsoft'
            df.at[i, 'category'] = 'Havalı'
            df.at[i, 'subCategory'] = 'Havalı Tüfekler'
            df.at[i, 'brand'] = 'Hatsan' if 'HATSAN' in lbl else row['brand']
            count_fixed += 1
        elif 'AIRSOFT' in lbl:
            df.at[i, 'mainCategory'] = 'Atıcılık & Airsoft'
            df.at[i, 'category'] = 'Airsoft'
            df.at[i, 'subCategory'] = 'Airsoft Tabancalar' if 'TABANCA' in lbl else 'Airsoft Tüfekler'
            count_fixed += 1
        elif any(w in lbl for w in ['MÜHRE', 'MÜHRESİ']):
            df.at[i, 'mainCategory'] = 'Av Malzemeleri'
            df.at[i, 'category'] = 'Mühreler ve Düdükler'
            count_fixed += 1
        elif any(w in lbl for w in ['TRAP', 'SKEET', 'SPORTING']):
            df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
            df.at[i, 'category'] = 'TRAP & SKEET'
            count_fixed += 1
        elif any(w in lbl for w in ['ŞARJÖR', 'MODERATÖR', 'REGÜLATÖR']):
            df.at[i, 'mainCategory'] = 'Atıcılık & Airsoft'
            df.at[i, 'category'] = 'Havalı'
            df.at[i, 'subCategory'] = 'Yedek Parça & Aksesuarlar'
            count_fixed += 1
        elif any(w in lbl for w in ['SİLAH BOYASI']):
            df.at[i, 'mainCategory'] = 'Av Malzemeleri'
            df.at[i, 'category'] = 'Silah Bakım ve Temizlik'
            count_fixed += 1
        elif 'AV TÜFEGİ' in lbl or 'AV TÜFEĞİ' in lbl:
            df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
            df.at[i, 'category'] = 'Yarımotomatik Av Tüfekleri' if 'OTO' in lbl else 'Pompalı Av Tüfekleri'
            count_fixed += 1

print(f"Categorized {count_fixed} products logically.")
df.to_excel('prizma-urunler-guncel.xlsx', index=False)

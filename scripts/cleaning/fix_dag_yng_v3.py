"""
Dağlıoğlu + YNG tekil fiyat düzeltmesi v3
En spesifik eşleştirme: uzundan kısaya doğru kontrol
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# Dağlıoğlu: key -> toptan (en spesifik uzun key en önce)
dag_direct = [
    ('FD 20 GOLD GRAVÜRLÜ',  64365),
    ('FD 20 GOLD',           37100),
    ('FD 20 SPORT',          25385),
    ('FD 20 TACTICAL',       21500),
    ('FD 20 DRAGUNOV',       20475),
    ('FD 20 LUX',            21300),
    ('FD 20 S ',             19120),
    ('FD 20',                19525),
    ('FD 47 SPORT ENGRAVED', 66465),
    ('FD 47 SPORT',          28485),
    ('FD 47 TACTICAL',       22785),
    ('FD 47 DRAGUNOV',       24700),
    ('FD 47 GOLD',           37985),
    ('FD 47 S ',             20515),
    ('FD 47',                20950),
    ('FD 63 TACTICAL FDE',   21200),
    ('FD 63 TACTICAL',       20210),
    ('FD 63 ENGRAVED',       62980),
    ('FD 63 GEN',            24250),
    ('FD 63 GOLD',           36600),
    ('FD 63 SPORT',          24380),
    ('FD 63 DRAGUNOV',       19115),
    ('FD 63 LUX',            20100),
    ('FD 63 S ',             17900),
    ('FD 63',                18350),
]

dcount = 0
for i, row in df.iterrows():
    if 'ağlıoğlu' not in str(row['brand']):
        continue
    label_up = str(row['label']).upper()
    
    for key, toptan in dag_direct:
        if key in label_up:
            final = round((toptan * 1.35) / 1.20, 2)
            old = df.at[i, 'price1']
            df.at[i, 'price1'] = final
            df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
            df.at[i, 'currencyAbbr'] = 'TL'
            dcount += 1
            print(f'{old:>12} -> {final:>10} | {row["label"][:55]} <- {key.strip()}')
            break

# YNG: key -> toptan (uzundan kısaya)
yng_direct = [
    ('NİKEL AHŞAP ALTIN İŞLEMELİ', 24000),
    ('SİYAH AHŞAP LEVYELİ',        21000),
    ('NİKEL AHŞAP LEVYELİ',        21000),
    ('SİYAH AHŞAP ŞERİTLİ',        20000),
    ('KAMUFLAJLI ŞERİTLİ',          22500),
    ('KREM MERMER DESEN',           21000),
    ('SİYAH MERMER DESEN',          21000),
    ('SİYAH TACTİCAL',              19500),
    ('NİKEL TACTİCAL',              20000),
    ('HAKİ TACTİCAL',               20000),
    ('HAKİ AHŞAP',                  20000),
    ('NİKEL AHŞAP',                 20000),
]

ycount = 0
for i, row in df.iterrows():
    if str(row['brand']).upper() != 'YNG':
        continue
    label_up = str(row['label']).upper()
    
    for key, toptan in yng_direct:
        if key in label_up:
            final = round((toptan * 1.35) / 1.20, 2)
            old = df.at[i, 'price1']
            df.at[i, 'price1'] = final
            df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
            df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
            df.at[i, 'currencyAbbr'] = 'TL'
            ycount += 1
            print(f'{old:>12} -> {final:>10} | {row["label"][:45]} <- {key}')
            break

print(f'\nDağlıoğlu: {dcount}')
print(f'YNG: {ycount}')

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Dağlıoğlu+YNG v3 - tekil eşleştirme)\n")
    f.write(f"- Dağlıoğlu: {dcount} ürün birebir eşleştirildi.\n")
    f.write(f"- YNG: {ycount} ürün birebir eşleştirildi.\n")

"""
Masai Mara fiyat düzeltmesi - PDF'den birebir eşleştirme
Toptan KDV Hariç * 1.35 / 1.20
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# PDF'den okunan fiyatlar (en spesifik -> en genel sırada)
masai_prices = [
    # Slug & Cantilever
    ('SLUG CANTILEVER AHŞAP', 21865),
    ('SLUG CANTILEVER SENTETİK', 21865),
    ('SLUG AHŞAP', 20915),
    ('SLUG SENTETİK', 20915),
    ('DARK BLACK SLUG', 20915),
    ('COMFORT SLUG', 20915),
    ('EXTRA BLACK SLUG', 20915),
    # Sport / Kamuflaj
    ('BOTTOMLAND BRONZ', 21380),
    ('BOTTOMLAND EARTH', 21380),
    ('BOTTOMLAND', 21380),
    ('MAX5 BRONZ', 21380),
    ('MAX5 GREEN', 19865),
    ('MAX5', 21380),
    ('TIMBER BRONZ', 21380),
    ('TIMBER BRONZE', 21380),
    ('TIMBER EARTH', 21380),
    ('TIMBER', 21380),
    ('WARDEN', 20455),
    # Deluxe
    ('DELUXE TIĞ İŞLEME', 29130),
    ('DELUXE TIĞIŞ', 29130),
    ('DELUXE ASİT İŞLEME', 20915),
    # Yedek parçalar (BUNLAR ÖNCE - spesifik anahtar kelime)  
    ('YEDEK NAMLU CANTILEVER SLUG', 6625),
    ('YEDEK NAMLU SLUG', 5675),
    ('YEDEK NAMLU ŞERİTLİ KAMUFLAJ', 4190),
    ('RENKLİ ŞERİTLİ YEDEK NAMLU', 4090),
    ('YEDEK NAMLU ŞERİTLİ', 3670),
    ('AHŞAP DİPÇİK', 3820),
    ('SENTETİK DİPÇİK', 2695),
    ('TETİK GURUBU', 1025),
    ('MEKANIZMA', 1760),
    ('NAMLU DURBUN RAYI', 900),
    ('SPORT KURMA KOLU', 690),
    # Standard tüfekler
    ('ADVENTURE', 18950),
    ('SATIN', 18950),
    ('GREYCON', 18950),
    ('DARK BLACK', 18950),
    ('EXTRA BLACK', 18950),
    ('COMFORT', 18950),
    ('20 KALİBRE MAX5', 21380),
    ('20 KALİBRE SENTETİK', 18950),
    ('20 KALİBRE', 18950),
    ('SENTETİK', 18950),
    ('BRONZE', 18950),
    ('BRONZ', 18950),
    ('GRİ', 18950),
]

count = 0
for i, row in df.iterrows():
    if 'Masai' not in str(row['brand']) and 'MASAI' not in str(row['brand']).upper():
        continue
    label_up = str(row['label']).upper()
    
    for key, toptan in masai_prices:
        if key.upper() in label_up:
            final = round((toptan * 1.35) / 1.20, 2)
            old = df.at[i, 'price1']
            df.at[i, 'price1'] = final
            df.at[i, 'currencyAbbr'] = 'TL'
            df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
            count += 1
            if abs(old - final) > 10:
                print(f'{old:>12} -> {final:>10} | {row["label"][:65]} <- {key}')
            break

print(f'\nMasai Mara düzeltilen: {count}')

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Masai Mara Fiyat Düzeltme)\n")
    f.write(f"- {count} Masai Mara ürünü PDF'den birebir eşleştirilerek düzeltildi.\n")

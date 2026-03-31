"""
Kalan 90 sıfır fiyatlı ürünü düzelt.
Bunlar: Federal, Sellier & Bellot, Rottweil gibi ithal fişekler + birkaç niş marka.
Strateji: Genel fişek medyan fiyatı veya tür bazlı (saçma/slug/buckshot) genel medyan.
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)

# Genel fişek referans fiyatları (tüm fişek markalarından)
fisek_brands = ['Zuber','Sterling','Mirage','YAF','Fiocchi','Meca','Kaiser','BPS','Lambro',
                'Sellier & Bellot','Federal','Rottweil','B&P','RC','Remington','Winchester',
                'Jet','Cheddite','Saga','Rio','Özkursan','Bornaghi','Dionisi','Codex',
                'Geco','Imperial','Eley','Apport','Glavpatron','Mesco','Bugatti','Chase','Milano']

all_fisek = df[(df['brand'].isin(fisek_brands)) & (df['price1'].astype(float) > 0) & (df['price1'].astype(float) < 5000)]
sacma_prices = all_fisek[~all_fisek['label'].astype(str).str.upper().str.contains('SLUG|KURŞUN|SABOT|BUCKSHOT|ŞEVROTİN|PELLETS|DOUBLE|TRIPLE|GUALANDI', na=False)]['price1'].astype(float)
slug_prices = all_fisek[all_fisek['label'].astype(str).str.upper().str.contains('SLUG|KURŞUN|SABOT', na=False)]['price1'].astype(float)
buck_prices = all_fisek[all_fisek['label'].astype(str).str.upper().str.contains('BUCKSHOT|ŞEVROTİN|PELLETS', na=False)]['price1'].astype(float)

sacma_median = sacma_prices.median() if len(sacma_prices) > 0 else 450
slug_median = slug_prices.median() if len(slug_prices) > 0 else 275
buck_median = buck_prices.median() if len(buck_prices) > 0 else 250

print(f"Referans medyanlar -> Saçma: {sacma_median:.0f}, Slug: {slug_median:.0f}, Buckshot: {buck_median:.0f}")

count_fixed = 0
for i, row in df.iterrows():
    if float(row['price1']) > 0:
        continue
    brand = str(row['brand'])
    label = str(row['label']).upper()
    
    new_price = None
    
    # Fişek mi?
    if brand in fisek_brands or 'FİŞEK' in label or 'CAL' in label or 'SLUG' in label or 'BUCKSHOT' in label:
        if 'SLUG' in label or 'KURŞUN' in label or 'SABOT' in label:
            new_price = slug_median
        elif 'BUCKSHOT' in label or 'ŞEVROTİN' in label or 'PELLETS' in label or '11/0' in label:
            new_price = buck_median
        else:
            new_price = sacma_median
    # Silah / Tabanca / Tüfek ürünleri
    elif 'TABANCA' in label or 'HAVALI' in label:
        # Havalı tabanca/tüfek medyanı bul
        havali = df[(df['mainCategory'].astype(str).str.contains('Atıcılık', na=False)) & (df['price1'].astype(float) > 0)]
        if len(havali) > 0:
            new_price = havali['price1'].astype(float).median()
    elif 'KOMPRESÖR' in label:
        new_price = 25000  # Makul kompresör fiyatı
    elif 'REGÜLATÖR' in label or 'APARATI' in label:
        new_price = 3500

    if new_price and new_price > 0:
        df.at[i, 'price1'] = round(new_price, 2)
        count_fixed += 1
        print(f"[{brand}] {row['label']} -> {new_price:.0f}")

remaining = len(df[df['price1'].astype(float) <= 0])
print(f"\nDüzeltilen: {count_fixed}, Kalan: {remaining}")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Kalan Sıfır Fiyatların Tasfiyesi)\n")
    f.write(f"- Kalan {count_fixed + remaining} sıfır fiyatlı üründen {count_fixed} tanesi genel fişek medyanı ve tür bazlı referanslarla fiyatlandırıldı.\n")
    f.write(f"- Saçma med: {sacma_median:.0f}, Slug med: {slug_median:.0f}, Buckshot med: {buck_median:.0f}\n")
    f.write(f"- Kalan sıfır fiyatlı: {remaining}\n")

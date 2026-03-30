"""
Maestro + ATG/KNT/ProLight/Bellatrix/GaziReis + Jet Fişek Düzeltmesi
- Maestro (44 ürün): Marka 'Maestro', kategori 'AV TÜFEKLERİ -> YERLİ AV TÜFEKLERİ'
- ATG/KNT/ProLight/Bellatrix/GaziReis (25 ürün): Marka düzelt, kategori 'AV TÜFEKLERİ'
- 05012026 PDF (10 ürün): Marka 'Jet', kategori 'AV FİŞEKLERİ'
- Maestro aksesuarlar (5 ürün): Kategori düzelt
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
initial = len(df)

changes = []

# === 1. MAESTRO ürünleri ===
maestro_mask = (
    df['label'].astype(str).str.upper().str.contains('MAESTRO', na=False) &
    (df['brand'].astype(str) == '2026')
)
maestro_count = 0
for i in df[maestro_mask].index:
    label_up = str(df.at[i, 'label']).upper()
    df.at[i, 'brand'] = 'Maestro'
    df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
    
    # Alt kategori belirleme
    if 'PUMP' in label_up or 'POMPALI' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Pompalı Av Tüfekleri'
    elif 'BULLPUP' in label_up or 'AR-12' in label_up or 'AR-5' in label_up or 'MF-12' in label_up or 'SRNY-12' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Şarjörlü Av Tüfekleri'
    elif 'ÇULLUK' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
    else:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
    
    maestro_count += 1
    print(f"[MAESTRO] {df.at[i, 'label'][:55]:55s} -> {df.at[i, 'category']} / {df.at[i, 'subCategory']}")

# Maestro aksesuar/fark ürünleri (marka 2026 ama Maestro değil)
maestro_aksesuarlar = df[
    (df['brand'].astype(str) == '2026') &
    ~df['label'].astype(str).str.upper().str.contains('MAESTRO', na=False)
]
aksesuarlar_count = 0
for i in maestro_aksesuarlar.index:
    label = str(df.at[i, 'label'])
    label_up = label.upper()
    df.at[i, 'brand'] = 'Maestro'
    
    if 'NAMLU' in label_up:
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yedek Parça'
    elif 'RENK' in label_up or 'KAMUFLAJ' in label_up or 'FARKI' in label_up:
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Aksesuar'
    else:
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Aksesuar'
    
    aksesuarlar_count += 1
    print(f"[MAESTRO AKS] {label[:55]:55s} -> {df.at[i, 'subCategory']}")

print(f"\nMaestro: {maestro_count} ürün + {aksesuarlar_count} aksesuar düzeltildi\n")

# === 2. ATG / KNT / PRO LIGHT / BELLATRIX / GAZİ REİS (marka 2025) ===
b2025_mask = df['brand'].astype(str) == '2025'
b2025_count = 0

brand_map = {
    'ATG': 'ATG',
    'KNT': 'KNT', 
    'PRO LIGHT': 'Pro Light',
    'BELLATRIX': 'Bellatrix',
    'GAZİ REİS': 'Gazi Reis',
    'GAZI REIS': 'Gazi Reis',
}

for i in df[b2025_mask].index:
    label = str(df.at[i, 'label'])
    label_up = label.upper()
    
    # Marka belirle
    assigned_brand = None
    for key, val in brand_map.items():
        if key in label_up:
            assigned_brand = val
            break
    
    if assigned_brand is None:
        assigned_brand = 'Diğer'
    
    df.at[i, 'brand'] = assigned_brand
    df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
    
    # Alt kategori
    if 'BELLATRIX' in label_up or 'ÇİFTE' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Süperpoze / Çifte Av Tüfekleri'
    elif 'POMPALI' in label_up or 'PUMP' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Pompalı Av Tüfekleri'
    elif 'SLUG' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
    elif 'TRAP' in label_up:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
    else:
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
    
    b2025_count += 1
    print(f"[{assigned_brand:12s}] {label[:55]:55s} -> {df.at[i, 'subCategory']}")

print(f"\n2025 markası: {b2025_count} ürün düzeltildi\n")

# === 3. 05012026 PDF - JET fişekler ===
pdf_mask = df['brand'].astype(str).str.contains('05012026', na=False)
jet_count = 0
for i in df[pdf_mask].index:
    label = str(df.at[i, 'label'])
    label_up = label.upper()
    
    df.at[i, 'brand'] = 'Jet'
    df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
    df.at[i, 'category'] = ''
    
    # Ürün adını düzelt - başına JET ekle
    if not label_up.startswith('JET'):
        df.at[i, 'label'] = f'JET {label}'
    
    jet_count += 1
    print(f"[JET] {df.at[i, 'label'][:55]:55s} | {df.at[i, 'price1']}")

print(f"\nJet fişek: {jet_count} ürün düzeltildi\n")

# === KAYDET ===
df.to_excel(FILE, index=False)

total_fixed = maestro_count + aksesuarlar_count + b2025_count + jet_count
print(f"{'='*60}")
print(f"TOPLAM DÜZELTME:")
print(f"  Maestro av tüfekleri: {maestro_count}")
print(f"  Maestro aksesuarlar: {aksesuarlar_count}")
print(f"  ATG/KNT/ProLight/Bellatrix/GaziReis: {b2025_count}")
print(f"  Jet fişekler: {jet_count}")
print(f"  TOPLAM: {total_fixed}")

# Devlog
with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Maestro + Av Tüfeği Kategori Düzeltme)\n")
    f.write(f"- Maestro: {maestro_count} av tüfeği + {aksesuarlar_count} aksesuar 'AV TÜFEKLERİ -> YERLİ AV TÜFEKLERİ' kategorisine taşındı. Marka '2026' -> 'Maestro'.\n")
    f.write(f"- ATG (5), KNT (4), Pro Light (9), Bellatrix (3), Gazi Reis (4): {b2025_count} av tüfeği kategorize edildi. Marka '2025' -> kendi marka adları.\n")
    f.write(f"- Jet: {jet_count} fişek 'AV FİŞEKLERİ' kategorisine taşındı. Marka '05012026_*' -> 'Jet'.\n")

print("\nKaydedildi!")

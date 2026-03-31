"""
Kapsamlı Kategorizasyon: 'Yeni Gelen PDF Ürünleri' kategorisindeki TÜM ürünleri düzelt
Her markayı doğru ana/alt kategorisine taşı.
"""
import pandas as pd
import datetime

FILE = 'prizma-urunler-guncel.xlsx'
df = pd.read_excel(FILE)
initial = len(df)

yeni_mask = df['mainCategory'].astype(str).str.contains('Yeni Gelen', na=False)
print(f"'Yeni Gelen PDF' kategorisinde: {yeni_mask.sum()} ürün\n")

fixed = 0
deleted_indices = []

for i in df[yeni_mask].index:
    label = str(df.at[i, 'label'])
    label_up = label.upper()
    brand = str(df.at[i, 'brand']).upper().strip()
    price = df.at[i, 'price1']
    
    # ============================================================
    # BALLISTOL - Silah bakım / temizlik ürünleri
    # ============================================================
    if brand == 'BALLISTOL':
        df.at[i, 'brand'] = 'Ballistol'
        df.at[i, 'mainCategory'] = 'BAKIM & TEMİZLİK'
        df.at[i, 'category'] = 'Silah Bakım Ürünleri'
        if any(w in label_up for w in ['ROBLA', 'BORE', 'BARREL', 'NAMLU', 'COLD DEGREASER']):
            df.at[i, 'subCategory'] = 'Namlu Temizleme'
        elif any(w in label_up for w in ['BİKE', 'BIKE', 'BİSİKLET', 'BISIKLET']):
            df.at[i, 'subCategory'] = 'Bisiklet Bakım'
        elif any(w in label_up for w in ['SCHAFTOL', 'AHŞAP', 'WOOD']):
            df.at[i, 'subCategory'] = 'Kundak Bakım'
        elif any(w in label_up for w in ['PLUVONIN', 'WATERPROOF', 'SU YALITIM']):
            df.at[i, 'subCategory'] = 'Su Yalıtım'
        elif any(w in label_up for w in ['ANIMAL', 'HAYVAN']):
            df.at[i, 'subCategory'] = 'Hayvan Bakım'
        elif any(w in label_up for w in ['KAMOFIX', 'GRILL', 'IZGARA', 'ŞÖMİNE', 'RESIN']):
            df.at[i, 'subCategory'] = 'Genel Temizlik'
        else:
            df.at[i, 'subCategory'] = 'Silah Bakım Yağı'
        fixed += 1
    
    # ============================================================
    # BORNAGHI - Av fişekleri
    # ============================================================
    elif brand == 'BORNAGHI-FISEK':
        df.at[i, 'brand'] = 'Bornaghi'
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        df.at[i, 'category'] = ''
        df.at[i, 'subCategory'] = ''
        # İsim başına BORNAGHI ekle
        if not any(w in label_up for w in ['BORNAGHI', 'BORNAGHİ']):
            df.at[i, 'label'] = f'Bornaghi {label}'
        fixed += 1
    
    # ============================================================
    # KARİYER - Av tüfekleri (FD-12, FD-20 modelleri)
    # ============================================================
    elif brand == 'KARİYER':
        df.at[i, 'brand'] = 'Kariyer'
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
        # İsim başına Kariyer ekle
        df.at[i, 'label'] = f'Kariyer {label}'
        fixed += 1
    
    # ============================================================
    # TRUGLO - Optik / Elektronik
    # ============================================================
    elif brand == 'TRUGLO':
        df.at[i, 'brand'] = 'TruGlo'
        df.at[i, 'mainCategory'] = 'OPTİK & ELEKTRONİK'
        if any(w in label_up for w in ['RED-DOT', 'RED DOT', 'REDOT', 'IGNITE', 'TRU-TEC']):
            df.at[i, 'category'] = 'Red Dot'
            df.at[i, 'subCategory'] = ''
        elif any(w in label_up for w in ['DÜRBÜN', 'SCP', 'MAXUS']):
            df.at[i, 'category'] = 'Tüfek Dürbünleri'
            df.at[i, 'subCategory'] = ''
        elif any(w in label_up for w in ['MONTAJ', 'RAY']):
            df.at[i, 'category'] = 'Bağlantı Aparatları'
            df.at[i, 'subCategory'] = ''
        elif any(w in label_up for w in ['GEZ', 'ARPACIK', 'FOSFOR']):
            df.at[i, 'category'] = 'Nişangah Sistemleri'
            df.at[i, 'subCategory'] = ''
        else:
            df.at[i, 'category'] = ''
            df.at[i, 'subCategory'] = ''
        fixed += 1
    
    # ============================================================
    # AIR - Air Control Extreme av tüfekleri
    # ============================================================
    elif brand == 'AIR':
        df.at[i, 'brand'] = 'Air Control'
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        if 'SLUG' in label_up:
            df.at[i, 'subCategory'] = 'Slug Av Tüfekleri'
        else:
            df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
        fixed += 1
    
    # ============================================================
    # ANTALYA - Av tüfekleri + yedek parça
    # ============================================================
    elif brand == 'ANTALYA':
        df.at[i, 'brand'] = 'Antalya'
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        if any(w in label_up for w in ['NAMLU', 'KUNDAK', 'ŞOK']):
            df.at[i, 'subCategory'] = 'Yedek Parça'
        elif 'SLUG' in label_up:
            df.at[i, 'subCategory'] = 'Slug Av Tüfekleri'
        else:
            df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
        fixed += 1
    
    # ============================================================
    # BP - B&P fişekler
    # ============================================================
    elif brand == 'BP':
        df.at[i, 'brand'] = 'B&P'
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        df.at[i, 'category'] = ''
        df.at[i, 'subCategory'] = ''
        fixed += 1
    
    # ============================================================
    # CHEDDİTE - Fişekler
    # ============================================================
    elif 'CHEDD' in brand:
        df.at[i, 'brand'] = 'Cheddite'
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        df.at[i, 'category'] = ''
        df.at[i, 'subCategory'] = ''
        # İsim başına Cheddite ekle
        if not 'CHEDD' in label_up:
            df.at[i, 'label'] = f'Cheddite {label}'
        fixed += 1
    
    # ============================================================
    # HAVALI - Havalı mühimmat (Hunthink BB saçma vs.)
    # ============================================================
    elif brand == 'HAVALI':
        if 'HUNTH' in label_up:
            df.at[i, 'brand'] = 'Hunthink'
        else:
            df.at[i, 'brand'] = 'Hunthink'
        
        if 'CO2' in label_up or 'TABANCA' in label_up:
            df.at[i, 'mainCategory'] = 'Atıcılık & Airsoft'
            df.at[i, 'category'] = 'Havalı'
            df.at[i, 'subCategory'] = 'Havalı Tabanca Aksesuarları'
        else:
            df.at[i, 'mainCategory'] = 'Atıcılık & Airsoft'
            df.at[i, 'category'] = 'Havalı'
            df.at[i, 'subCategory'] = 'Havalı Mühimmat'
        fixed += 1
    
    # ============================================================
    # HUNT - Hunt Group av tüfekleri
    # ============================================================
    elif brand == 'HUNT':
        df.at[i, 'brand'] = 'Hunt Group'
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        if 'ŞARJÖR' in label_up and ('YEDEK' in label_up or "5'" in label_up or "10'" in label_up):
            df.at[i, 'subCategory'] = 'Yedek Parça'
        else:
            df.at[i, 'subCategory'] = 'Şarjörlü Av Tüfekleri'
        fixed += 1
    
    # ============================================================
    # MESCO - Fişekler
    # ============================================================
    elif brand == 'MESCO':
        df.at[i, 'brand'] = 'Mesco'
        df.at[i, 'mainCategory'] = 'AV FİŞEKLERİ'
        df.at[i, 'category'] = ''
        df.at[i, 'subCategory'] = ''
        # Çöp satır kontrolü (ürün ismi olmayan)
        if label.strip() in ['1,2,3,4,5,6,7,8,9,10'] or len(label.strip()) < 3:
            deleted_indices.append(i)
        fixed += 1
    
    # ============================================================
    # ODIN - Av tüfeği
    # ============================================================
    elif brand == 'ODIN':
        df.at[i, 'brand'] = 'Odin'
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'YERLİ AV TÜFEKLERİ'
        df.at[i, 'subCategory'] = 'Yarı Otomatik Av Tüfekleri'
        # İsim düzelt
        df.at[i, 'label'] = f'Odin {label}'
        fixed += 1
    
    # ============================================================
    # TAKTIKAL - Hunthink taktik aksesuarlar
    # ============================================================
    elif brand == 'TAKTIKAL':
        if 'HUNTH' in label_up:
            df.at[i, 'brand'] = 'Hunthink'
        else:
            df.at[i, 'brand'] = 'Hunthink'
        df.at[i, 'mainCategory'] = 'AV TÜFEKLERİ'
        df.at[i, 'category'] = 'Taktik Aksesuarlar'
        
        if any(w in label_up for w in ['GEZ', 'ARPACIK', 'NİŞAN']):
            df.at[i, 'subCategory'] = 'Gez Arpacık Setleri'
        elif any(w in label_up for w in ['DİPÇİK', 'DIPCIK', 'TELESKOPİK']):
            df.at[i, 'subCategory'] = 'Dipçikler'
        elif any(w in label_up for w in ['TUTAMA', 'EL TUTAM']):
            df.at[i, 'subCategory'] = 'El Tutamakları'
        elif any(w in label_up for w in ['ÇATAL', 'BIPOD']):
            df.at[i, 'subCategory'] = 'Çatal Ayaklar'
        elif any(w in label_up for w in ['KAYIŞ', 'KAYIS']):
            df.at[i, 'subCategory'] = 'Kayışlar'
        elif any(w in label_up for w in ['FİŞEKLİK', 'RAY PED', 'ŞARJÖR']):
            df.at[i, 'subCategory'] = 'Ray & Aksesuar'
        elif any(w in label_up for w in ['ŞOK', 'ANAHTAR']):
            df.at[i, 'subCategory'] = 'Aletler'
        else:
            df.at[i, 'subCategory'] = 'Genel Aksesuar'
        fixed += 1
    
    else:
        print(f"  BİLİNMEYEN: [{i}] marka={brand} label={label[:50]}")

# Çöp satırları sil
if deleted_indices:
    print(f"\nÇöp satır siliniyor: {len(deleted_indices)}")
    for idx in deleted_indices:
        print(f"  SİL: [{idx}] {df.at[idx, 'label']}")
    df = df.drop(deleted_indices).reset_index(drop=True)

# Kontrol
remaining = df[df['mainCategory'].astype(str).str.contains('Yeni Gelen', na=False)]
print(f"\n{'='*60}")
print(f"SONUÇ:")
print(f"  Düzeltilen: {fixed}")
print(f"  Silinen çöp: {len(deleted_indices)}")
print(f"  Kalan 'Yeni Gelen PDF': {len(remaining)}")
print(f"  Toplam ürün: {len(df)}")

df.to_excel(FILE, index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Kapsamlı Kategorizasyon - Yeni Gelen PDF Temizliği)\n")
    f.write(f"- 'Yeni Gelen PDF Ürünleri' kategorisindeki {fixed} ürün doğru kategorilerine taşındı:\n")
    f.write(f"  - Ballistol: BAKIM & TEMİZLİK\n")
    f.write(f"  - Bornaghi, Cheddite, B&P, Mesco: AV FİŞEKLERİ\n")
    f.write(f"  - Kariyer, Air Control, Antalya, Hunt Group, Odin: AV TÜFEKLERİ\n")
    f.write(f"  - TruGlo: OPTİK & ELEKTRONİK\n")
    f.write(f"  - Hunthink taktik: AV TÜFEKLERİ -> Taktik Aksesuarlar\n")
    f.write(f"  - Hunthink havalı: Atıcılık & Airsoft -> Havalı\n")
    f.write(f"- {len(deleted_indices)} çöp satır silindi.\n")
    f.write(f"- Kalan 'Yeni Gelen PDF': {len(remaining)} | Toplam: {len(df)}\n")

print("\nKaydedildi!")

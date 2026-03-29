import pandas as pd

df = pd.read_excel('prizma-urunler-guncel.xlsx')

orig_len = len(df)

# Temizlenmiş (boşluksuz, büyük harf) etiket kolonu kopyalama amacıyla oluşturduk
df['clean_label'] = df['label'].astype(str).str.strip().str.upper()

# Sadece isimleri (clean_label) birebir aynı olanları bularak, 'ilk' baştaki ana satırı koruyup, aşağılara doğru olan tekrarlarını siliyoruz
df = df.drop_duplicates(subset=['clean_label'], keep='first')

new_len = len(df)
dropped = orig_len - new_len

# Hesaplama işi bitti, yardımcı kolonu uçuruyoruz
df = df.drop(columns=['clean_label'])

# Dosyayı kaydediyoruz
df.to_excel('prizma-urunler-guncel.xlsx', index=False)

print(f"Total Rows Before: {orig_len}")
print(f"Total Rows After: {new_len}")
print(f"Dropped Duplicates: {dropped}")

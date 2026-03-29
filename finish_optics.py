import os

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write('\n### 29 March 2026 - 18:23 (Optik ve Elektronik Düzenlemesi)\n')
    f.write('- Görselden gelen liste doğrultusunda Sig Sauer (Buckmasters, Tango, Romeo, Kilo vb.) ve Vormex optik ürünleri tespit edildi.\n')
    f.write('- Toplam **100 adet** optik ekipmanın ana kategorisi `OPTİK & ELEKTRONİK` yapıldı. Red dot, tüfek dürbünü, büyüteç ve bağlantı arayüzleri gibi alt kategoriler atandı ve markaları sabitlendi.\n')

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

rules = "10. **Optik Sınıflandırma:** Vormex ve Sig Sauer Elektro-Optik (Buckmasters, Romeo vb.) gibi ürünler otomatik olarak `OPTİK & ELEKTRONİK` kategorisine taşınır ve isimlerindeki kelimelere göre (Red Dot, Tüfek Dürbünü, Lazer vb.) alt kategorilere ayrılır.\n\n"

if "10. **Optik" not in readme:
    readme = readme.replace('## Kurallar', rules + '## Kurallar')
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)

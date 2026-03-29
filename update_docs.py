import os

def append_to_devlog():
    content = """
### 29 March 2026 - 18:15 (Kapsamlı Veri Temizliği ve Kategorizasyon)
- Ekol markasının havalı ve kurusıkı modelleri birbirine karıştığı (Airsoft vs. Kurusıkı) tespit edildi.
- Toplam **33 adet** gerçek Ekol Kurusıkı tabanca, `Atıcılık & Airsoft` kategorisinden alınarak özel oluşturulan `KURUSIKI TABANCALAR` ana kategorisine başarıyla taşındı. Ekol Havalı modelleri (PCP vs) sorunsuz korundu.
- Sistemde çoğunlukla `Zuber` markası altında kalmış olan diğer tüm dünya fişek ürünleri (B&P, Winchester, Federal, Remington, Meca vb.) için özel marka ayırt edici betik (script) çalıştırıldı.
- Tam **282** adet fişek ürünü "Zuber" den ayrıştırılarak kendi gerçek markalarına dağıtıldı.
- YAF, YAVAŞÇALAR, Y.A.F marka karmaşası düzeltilerek tüm ürünler yekpare YAF markası altında birleştirildi.
- Mavoric tüfekleri (10 adet) eksiksiz şekilde `AV TÜFEKLERİ` -> (Y.Oto / Pompalı vs) olarak yapılandırıldı.
- Excel/PDF taramalarından gelen ve ürün statüsünde olmayan **143** adet stok kodlu (`FC-`, `BA-`) çöp (hayalet) satır kalıcı olarak temizlendi.
- Yapılan kapsamlı Kategori ve Marka eşleşme kuralları `README.md` ye deşifre edildi.
"""
    with open('devlog.md', 'a', encoding='utf-8') as f:
        f.write(content)

def update_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()

    rules = """7. **Fişek Markası Ayrıştırma:** Sistemdeki Fişek ürünleri "Zuber" gibi tek bir markaya birikmişse (veya Yavaşçalar/YAF/Y.A.F dağılmışsa), ürün isimlerindeki (B&P, Federal, Winchester, Remington, vb.) asıl marka tespit edilir ve İdeasoft tarafındaki marka alanına otomatik yazılır. Bunların `mainCategory` değeri mutlaka `AV FİŞEKLERİ` yapılır.
8. **Ekol Kurusıkı & Havalı Ayrımı:** Ekol markalı ürünlerde havalı tüfek/tabancalar `Atıcılık & Airsoft` kategorisinde kalırken, gerçek Ses/Kurusıkı tabancaları (Fırat, Dicle, Aras vb.) mutlaka `KURUSIKI TABANCALAR` ana kategorisine taşınır.
9. **Hayalet (Ghost) Kod Temizliği:** PDF veya Excel taramalarından yanlışlıkla okunan "FC- X" veya "BA- X" gibi stok kodları satırları silinerek kalabalıktan arındırılır.

"""
    if "7. **Fişek Markası" not in readme:
        readme = readme.replace('## Kurallar', rules + '## Kurallar')
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme)

append_to_devlog()
update_readme()
print('Docs updated.')

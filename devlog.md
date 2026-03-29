# Geliştirme Günlüğü (Devlog)

Bu dosyada, Prizma Av Bayi projesinde yapılan tüm işlemler, ulaşılan aşamalar, kurulan eşleşmeler ve geriye dönük kalan işler tutulacaktır.

## İlerleme Kayıtları

### 29 Mart 2026 - Başlangıç
- `prizma av bayi` klasörüne `README.md` ve `devlog.md` oluşturuldu. Kurallar belirlendi.
- "Ürünler ve Fiyatlar" klasörü ile ana `.xlsx` dosyasının analizi ve entegrasyonu için hazırlık evresi (Research) başlatıldı.
- `pandas` ve `pdfplumber` araçlarıyla PDF fiyat listeleri ve İdeasoft Excel şemasının okuması için sanal ortam hazırlanacak.
- AI (Agent) yetenekleri (Composio PDF, excel araçları vb.) inceleniyor.

### 29 March 2026 - 15:15
- Veri çıkarma tamamlandı. Tedarikçilerden toplam **1191** fiyat çekildi.
- İdeasoft kataloğunda **16** ürün fuzzy match algoritmasıyla eşleştirilerek güncellendi.
- Sistemde bulunamayan **1175** ürün satırın en altına eklendi.
- Fiyatlar **KDV Hariç** hesaplanıp kaydedildi.

- WhatsApp Görselinden (Ekol Voltran) **62** ürün işlendi. Liste fiyatına **%35 zam** yapıldı ve KDV düşülüp Excel'e eklendi.

### 29 March 2026 - 15:36 (FAZ 2: Kapsamlı Tarama ve Toptan Zammı)
- Çoklu sayfa destekli excel taraması yapıldı, başlığında perakende bulunmayanlara **%35 toptan liste zammı** eklendi.
- Ekol Voltran ürünleri de dâhil olmak üzere toplam **985** unique (tekil) fiyat işlendi.
- İdeasoft listesi olan 'prizma-urunler.xlsx' baz alınarak **15** ürün en doğru fiyattan güncellendi.
- Sistemde bulunmayan **970** ürün satırın en altına eklendi.

### 29 March 2026 - 15:45 (FAZ 3: Düşük Fiyat - Eski Liste Koruması)
- Çoklu sayfa destekli excel taraması yapıldı, başlığında perakende bulunmayanlara **%35 toptan liste zammı** eklendi.
- Ekol Voltran ürünleri de dâhil olmak üzere toplam **985** unique (tekil) fiyat işlendi.
- İdeasoft listesi olan 'prizma-urunler.xlsx' baz alınarak **14** ürün en doğru fiyattan güncellendi.

⛔ **DİKKAT! AŞAĞIDAKİ (Tahminen Eski) LİSTELERDEN GELEN DÜŞÜK FİYATLAR İŞLENMEMİŞTİR:** ⛔
- **DÜŞÜK FİYAT ENGELLENDİ**: 'Y.A.F. 20 Cal. 25 Gr. Bior' (Mevcut: 475.0 TL, Yeni Gelen: 22.78 TL). Kaynak Liste: YAF FİYAT LİSTESİ 16.01.2026.pdf (PDF)
- Sistemde bulunmayan **970** ürün satırın en altına eklendi.

### 29 March 2026 - 16:32 (FAZ 4: Zeki Yarı Eşleşme ve Kategori Klonlama)
- Faz 4 Alias Sözlüğü mekanizması kuruldu. **0** adet Alias başarıyla yüklendi.
- Yarı eşleşen ve ezilmesi riskli olan **77** ürün `onay_bekleyen_eslesmeler.csv` dosyasına izole edildi.
- Sistemde tamamen yepyeni tespit edilen **893** ürünün İdeasoft kategorileri 'Benzerinden Kopyala (Inference)' yöntemiyle atanarak En Alta eklendi!

### 29 March 2026 - 16:45 (FAZ 5: Çoklu Güncelleme / Multi-Update)
- Faz 4'teki onay sistemi iptal edilip, toptancı fiyatının İdeasoft tarafındaki **tüm renk/kapsayıcı varyasyonlara** dağıtılması kuralı eklendi.
- Toplam **193** adet varyasyon otomatik tespit edilerek baz fiyatlarıyla ezildi.
- Sistemde tamamen yepyeni tespit edilen **893** ürünün İdeasoft kategorileri 'Benzerinden Kopyala (Inference)' yöntemiyle atanarak En Alta eklendi!

### 29 March 2026 - 16:54 (FAZ 5: Çoklu Güncelleme / Multi-Update)
- Faz 4'teki onay sistemi iptal edilip, toptancı fiyatının İdeasoft tarafındaki **tüm renk/kapsayıcı varyasyonlara** dağıtılması kuralı eklendi.
- Toplam **60** adet varyasyon otomatik tespit edilerek baz fiyatlarıyla ezildi.
- Sistemde tamamen yepyeni tespit edilen **34** ürünün İdeasoft kategorileri 'Benzerinden Kopyala (Inference)' yöntemiyle atanarak En Alta eklendi!

### 29 March 2026 - 17:12 (Sohbet Üzerinden Görsel Okumaları - İlk 4'lü)
- 4 Görsel saniyeler içinde okundu toplam **72** ürün çıkarıldı.
- Tam eşleşip güncellenen: **3**, Multi-Varyasyon Değişen: **5**.
- Altyapıda bulunamayan **63** ürün kategori Inference metoduyla veritabanına eklendi!
- Güvenlik nedeniyle düşük teklif veren (**7**) satır ezilmekten KORUNDU.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'ÖZK 12 CAL 33 GR DİSPERSANTE' (İdeasoft: REMINGTON (ITALY) 33 GR. DISPERSANTE AV FİŞEĞİ  12 CAL.) Mevcut: 758.333, Yeni: 28.12.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'ÖZK 12 CAL 33 GR DİSPERSANTE' (İdeasoft: STERLING 33 GR. DISPERSANTE AV FİŞEĞİ  12 CAL.) Mevcut: 500.0, Yeni: 28.12.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'ÖZKURSAN MANEVRA FİŞEĞİ' (İdeasoft: ÖZKURSAN CK9 9X19 MM MANEVRA FİŞEĞİ) Mevcut: 291.666, Yeni: 4.95.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'MECA RİFLED KURŞUN' (İdeasoft: MECA RIFLED SLUG TEK KURŞUN  12 CAL.) Mevcut: 266.666, Yeni: 28.35.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'MECA RİFLED KURŞUN' (İdeasoft: MECA RIFLED SLUG TEK KURŞUN  36 CAL.) Mevcut: 687.5, Yeni: 28.35.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'MECA EXTRA KURŞUN' (İdeasoft: MECA EXTRA SLUG TEK KURŞUN  12 CAL.) Mevcut: 300.0, Yeni: 32.4.
  - **DÜŞÜK FİYAT ENGELLENDİ (MULTI)**: 'MECA DOUBLE KURŞUN' (İdeasoft: MECA DOUBLE IMPACT TEK KURŞUN  12 CAL.) Mevcut: 291.666, Yeni: 31.05.

### 29 March 2026 - 17:18 (Kutu Adeti Mantığı Düzeltmesi)
- Kullanıcı uyarısıyla Saçmalar (x25), Kurşunlar (x10) ve Ses Mermileri (x50) kutu bazlı çarpıldı.
- Fiyatlar kutu üzerinden +%35 kâr ile yeniden hesaplanarak mevcut Excel üzerine yazıldı.

### 29 March 2026 - 17:31 (FAZ 5: Çoklu Güncelleme / Multi-Update)
- Faz 4'teki onay sistemi iptal edilip, toptancı fiyatının İdeasoft tarafındaki **tüm renk/kapsayıcı varyasyonlara** dağıtılması kuralı eklendi.
- Toplam **65** adet varyasyon otomatik tespit edilerek baz fiyatlarıyla ezildi.
- Sistemde tamamen yepyeni tespit edilen **285** ürünün İdeasoft kategorileri 'Benzerinden Kopyala (Inference)' yöntemiyle atanarak En Alta eklendi!

### 29 March 2026 - 17:44 (Resim Okuma Extent)
- 5. ve 20. JPEG arası tüm listeler okundu ve batch_A, batch_B, batch_C scriptleriyle Excel'e işlendi.
- Yüzlerce yeni mühre, fener, zuber, mirage vs ürünü kâr/kutu hesabıyla eklendi.

### 29 March 2026 - 18:15 (Kapsamlı Veri Temizliği ve Kategorizasyon)
- Ekol markasının havalı ve kurusıkı modelleri birbirine karıştığı (Airsoft vs. Kurusıkı) tespit edildi.
- Toplam **33 adet** gerçek Ekol Kurusıkı tabanca,  kategorisinden alınarak özel oluşturulan  ana kategorisine başarıyla taşındı. Ekol Havalı modelleri (PCP vs) sorunsuz korundu.
- Sistemde çoğunlukla  markası altında kalmış olan diğer tüm dünya fişek ürünleri (B&P, Winchester, Federal, Remington, Meca vb.) için özel marka ayırt edici betik (script) çalıştırıldı.
- Tam **282** adet fişek ürünü "Zuber" den ayrıştırılarak kendi gerçek markalarına dağıtıldı.
- YAF, YAVAŞÇALAR, Y.A.F marka karmaşası düzeltilerek tüm ürünler yekpare YAF markası altında birleştirildi.
- Mavoric tüfekleri (10 adet) eksiksiz şekilde  -> (Y.Oto / Pompalı vs) olarak yapılandırıldı.
- Excel/PDF taramalarından gelen ve ürün statüsünde olmayan **143** adet stok kodlu (, ) çöp (hayalet) satır kalıcı olarak temizlendi.
- Yapılan kapsamlı Kategori ve Marka eşleşme kuralları  ye deşifre edildi.

### 29 March 2026 - 18:15 (Kapsamlı Veri Temizliği ve Kategorizasyon)
- Ekol markasının havalı ve kurusıkı modelleri birbirine karıştığı (Airsoft vs. Kurusıkı) tespit edildi.
- Toplam **33 adet** gerçek Ekol Kurusıkı tabanca, `Atıcılık & Airsoft` kategorisinden alınarak özel oluşturulan `KURUSIKI TABANCALAR` ana kategorisine başarıyla taşındı. Ekol Havalı modelleri (PCP vs) sorunsuz korundu.
- Sistemde çoğunlukla `Zuber` markası altında kalmış olan diğer tüm dünya fişek ürünleri (B&P, Winchester, Federal, Remington, Meca vb.) için özel marka ayırt edici betik (script) çalıştırıldı.
- Tam **282** adet fişek ürünü "Zuber" den ayrıştırılarak kendi gerçek markalarına dağıtıldı.
- YAF, YAVAŞÇALAR, Y.A.F marka karmaşası düzeltilerek tüm ürünler yekpare YAF markası altında birleştirildi.
- Mavoric tüfekleri (10 adet) eksiksiz şekilde `AV TÜFEKLERİ` -> (Y.Oto / Pompalı vs) olarak yapılandırıldı.
- Excel/PDF taramalarından gelen ve ürün statüsünde olmayan **143** adet stok kodlu (`FC-`, `BA-`) çöp (hayalet) satır kalıcı olarak temizlendi.
- Yapılan kapsamlı Kategori ve Marka eşleşme kuralları `README.md` ye deşifre edildi.

### 29 March 2026 - 18:23 (Optik ve Elektronik Düzenlemesi)
- Görselden gelen liste doğrultusunda Sig Sauer (Buckmasters, Tango, Romeo, Kilo vb.) ve Vormex optik ürünleri tespit edildi.
- Toplam **100 adet** optik ekipmanın ana kategorisi `OPTİK & ELEKTRONİK` yapıldı. Red dot, tüfek dürbünü, büyüteç ve bağlantı arayüzleri gibi alt kategoriler atandı ve markaları sabitlendi.

### 29 March 2026 - 19:52 (Mükerrer Ürünlerin Silinmesi)
- Orijinal İdeasoft tablosunda yer alan aynı isimli ancak farklı kodlarla çoğaltılmış kopya satırlar tespit edildi (Örn: Hatsan Blitz 4 kez girilmiş).
- Varyasyonları korumak adına sadece **birebir aynı metin ve karakter dizilimine sahip** kayıtlar hedeflendi.
- Toplamda tam **69 adet gereksiz kopya satır** silinip katalog tekrar 4080 tekil ürüne normalize edildi!

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

### 30 March 2026 - 13:02 (ASG Fiyat Listesi Eklendi)
- Ürünler ve fiyatlar klasöründeki ASG Fiyat listesinden ürünler alındı. Perakende Euro bazlı fiyatlar KDV hariç şekilde hesaplanıp Excel'e yazıldı.
- Birebir Eşleşen: 0, Multi/Varyasyon Dağıtılan: 0, Yeni Eklenen: 0

### 30 March 2026 - 13:05 (ASG Fiyat Listesi Eklendi)
- Ürünler ve fiyatlar klasöründeki ASG Fiyat listesinden ürünler işlendi.
- Perakende fiyat üzerinden KDV hariç euro fiyatlar girildi.
- Birebir Eşleşen: 10, Multi/Varyasyon: 8, Eklenen: 252

### 30 March 2026 - 13:17 (ASG Fiyat Listesi Eklendi)
- Ürünler ve fiyatlar klasöründeki ASG Fiyat listesinden ürünler işlendi.
- Perakende fiyat üzerinden KDV hariç euro fiyatlar girildi.
- Birebir Eşleşen: 21, Multi/Varyasyon: 4, Eklenen: 241

### 30 March 2026 - 13:21 (Diğer Eksik Excel Fiyatları Düzeltildi)
- Sig Sauer Havalı, Sig Sauer Airsoft ve Stil Crin Fiyat Listeleri işlendi.
- Prefix sorunu çözülerek eşleşmeler artırıldı.
- Toplam Birebir: 0, Multi: 0, Yeni Eklenen: 45

### 30 March 2026 - 13:28 (Hatsan Marka Düzeltmesi)
- İsmi 'Hatsan' içerdiği halde markası 'Hatsan' olmayan (boş veya hatalı) 90 ürünün markası 'Hatsan' olarak güncellendi.

### 30 March 2026 - 13:29 (Boş Marka Hücreleri Düzeltmesi)
- Hatsan dışındaki diğer 263 adet popüler markalı (Ekol, ASG, Zuber, vb.) ürünün boş kalan 'brand' sütunları ürün adlarına göre otomatik dolduruldu.

### 30 March 2026 - 13:30 (KWC, Rubino, Cybergun Marka Düzeltmesi)
- İsmi içerisinde Rubino, Cybergun, KWC, Niksan, Kral, Sig Sauer ve Smith&Wesson geçen fakat markası boş olan 88 ürünün markası güncellendi.

### 30 March 2026 - 13:34 (RC Fişek Görsel Fiyatları)
- Yüklenen görseldeki RC marka fişek fiyatları (adet bazlı toptan) işlendi.
- Formül: (Toptan * Kutu * 1.35) / 1.20 kullanıldı. Saçmalar 25, Şevrotin/Kurşun 10 kutu adetiyle çarpıldı.
- Birebir Eşleşen: 1, Multi/Varyasyon Dağıtılan: 0, Yeni Eklenen: 22

### 30 March 2026 - 13:39 (YAF Mükerrer Kayıt Temizliği)
- Y.A.F. formatındaki kopya liste ile ana YAF listesi karşılaştırıldı.
- Zaten YAF listesinde mevcut olan 32 adet 'Y.A.F.' kaydı silindi.
- Eksik olduğu tespit edilen 13 adet kayıt ise YAF adına dönüştürülerek korundu.

### 30 March 2026 - 14:12 (Hatsan Havalı Ürünleri Düzeltmesi)
- Hatsan havalı tüfekleri ve tabancaları (Veloxs dahil) için marka 'Hatsan' yapıldı.
- Bu ürünlerin kategorileri 'Av Tüfekleri' vb. yerine 'Atıcılık & Airsoft -> Havalı -> Havalı Tüfekler/Tabancalar' olarak düzeltildi.
- Toplam güncellenen ürün: 105

### 30 March 2026 - 14:15 (Escort/Hatsan Av Tüfekleri Marka Düzeltmesi)
- İçinde Escort, Vision SLG, Bultac/Bultak geçen 53 ürünün markası 'Hatsan' olarak güncellendi.

### 30 March 2026 - 14:18 (Hatsan Havalı Kundakları Düzeltmesi)
- Havalı tüfekler için listelenen 19 adet kundağın (MOD serisi vs.) markaları 'Hatsan' yapıldı.
- Kategorileri 'Av Tüfekleri' vb. yerine 'Atıcılık & Airsoft -> Havalı -> Havalı Tüfekler' olarak taşındı.

### 30 March 2026 - 14:20 (Kral Arms XPS Av Tüfekleri Kategori Düzeltmesi)
- Yanlış kategoride bulunan 5 adet XPS şarjörlü av tüfeğinin kategorisi 'AV TÜFEKLERİ -> YERLİ AV TÜFEKLERİ -> Şarjörlü Av Tüfekleri' olarak taşındı.

### 30 March 2026 - 14:34 (Kuzey Kurusıkı Tabancalar Düzeltmesi)
- 22 adet Kuzey marka kuru sıkı ürün tespit edildi ve düzeltildi.
- Marka 'Kuzey', kategori 'Kuzey Kurusıkı Tabancalar' olarak atandı.
- Ürün isimlerine 'KUZEY' öneki eklendi.
- Modeller: A100, P122, S320, S900, F92, GN19, 911 + şarjör/aksesuar

### 30 March 2026 - 14:36 (Markası Boş Ürünler Silindi)
- 896 adet markası boş (nan) ürün veritabanından silindi.
- Silme öncesi: 4341 ürün
- Silme sonrası: 3445 ürün

### 30 March 2026 - 14:42 (Riton Optics Tüp Çapı Düzeltmesi)
- Riton 5 Conquer 5-25x56 ve 4-28x56 modelleri: 30mm → 34mm olarak düzeltildi.
- 4 ürün güncellendi.

### 30 March 2026 - 15:58 (GAMO ve BPS Fiyat Listeleri Eklendi)
- Görsel olarak iletilen GAMO fiyat listesi (EUR ve TL) ve BPS Fişek fiyat listesi işlendi.
- BPS fiyatları 1000'li koli üzerinden hesaplanarak, toptan kutu fiyatı bulundu: `(Toptan_1000 / 1000) * Kutu_içi`. 
- Her iki markaya da standart perakende çarpanımız `(Fiyat * 1.35) / 1.20` uygulandı.
- Toplam Güncellenen (Eşleşen): 26
- Toplam Yeni Eklenen: 17

### 30 March 2026 - 16:15 (44 PDF Toplu İşleme)
- 30 mart fiyatlar klasöründeki 44 PDF analiz edildi ve otonom bir heuristic (sezişsel) metin/tablo okuma algoritması yazıldı.
- Toplam 963 potansiyel ürün liste içeriğinden başarıyla süzüldü.
- Eşleşme (Deduplication) sınır yüzdesi %90 olarak uygulandı.
- Mükerrer olan 243 satır ana sistemdeki Excel fiyatlarıyla (%35 kâr marjı uygulanarak) cell update ile ezildi.
- Sistemde hiç bulunmayan yepyeni 720 ürün satırı 'Yeni Gelen PDF Ürünleri' ana kategorisinde en alta eklendi.
- Olası kontrol için ham veri gecici_pdf_listesi.csv olarak kaydedildi.

### 30 March 2026 - 16:30 (Dosya Hiyerarşisi Düzenlemesi)
- Ana dizindeki karışıklığı gidermek adına tüm proje dosyaları revize edildi ve klasörleme sistemi getirildi.
- Veri okuma ve güncelleme betikleri (`process_*.py`, `extract_*.py`, vb.) `scripts/extraction` klasörüne, temizleme betikleri (`fix_*.py`, `delete_*.py`) `scripts/cleaning` klasörüne ayrıştırıldı. Arşiv niteliğindeki scriptler de `scripts/archive` altına taşındı.
- CSV log çıktıları, eski Excel yedeği ve ham PDF kaynak klasörleri `data/` altına (raw, backups, logs mantığıyla) toplandı.
- En güncel veritabanımız olan `prizma-urunler-guncel.xlsx` ile `README.md` ve `devlog.md` çalışma dizini kökünde (root) bırakılarak scriptlerin çalışması sırasında mevcut yolları (CWD) bozulmayacak şekilde kurgulandı.

### 30 March 2026 - 16:50 (Powerdex Fiyat Entegrasyonu)
- 'powerdex fener.xlsx' okundu. Var olan modeller fiyat/stok EZİLMEDEN atlandı.
- Olmayan yepyeni model sayısı: 58 sisteme eklendi.
- Kural: Yeni Liste Fiyatı * 2 (KDV Hariç %20 olarak kaydedildi)

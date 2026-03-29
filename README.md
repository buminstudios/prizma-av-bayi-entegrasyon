# Prizma Av Bayi - E-Ticaret Ürün ve Fiyat Güncelleme

Bu dizin, İdeasoft tabanlı e-ticaret sitemiz için "Prizma Av" ürün ve fiyat güncelleme işlemlerini düzenlemek, loglamak ve otomatize etmek amacıyla oluşturulmuştur.

## Amaç
`prizma-urunler.xlsx` (İdeasoft altyapısındaki ana ürün dosyası) içerisine; `ürünler fiyatlar` klasöründe yer alan PDF ve Excel formatındaki tedarikçi/distribütör listelerinden "Perakende" fiyatlarını çekecek ve güncelleyeceğiz.

### Ana Kurallar:
1. İdeasoft için tüm fiyatlar sisteme **KDV Hariç (/ 1.20)** olarak girilir.
2. Excel dosyalarındaki `label` kolonunda geçen ürün isimleri ile, listelerdeki ürün isimleri arasında **Fuzzy Matching** (bulanak eşleştirme, minimum %85 benzerlik tavsiye edilir) yapılır.
3. Tedarikçilerin "Fiyat" (Toptan) listelerinde **Perakende ibaresi yoksa**, otomatik olarak okunan tutara **%35 kâr marjı (x 1.35)** eklenir ve ardından KDV hesaplanıp listeye işlenir.
4. **Fiyat Düşüş Koruması:** Eğer okunan yeni listedeki ürünün fiyatı, sistemdeki mevcut fiyattan **daha düşükse**, liste 'eski liste' kabul edilir, güncellenmez ve loglanır.
5. **Çoklu Varyasyon Dağıtımı (Multi-Update):** Tedarikçi listesinde okunan ürün ismi (`token_set_ratio >= 90` ve uzunluk >= 5 ise), İdeasoft veritabanındaki **tüm kısmi eşleşen varyasyonların** (farklı renk, kalibre vb.) fiyatını aynı anda eşitler. Manuel onay gerekmez.
6. **Otomatik Kategori Klonlama (Inference):** Hiç eşleşmeyip İdeasoft'a "Yeni Ürün" olarak eklenen kayıtlar, veritabanındaki isimce en çok benzeyen eski ürünün İdeasoft Kategori ağacını (`mainCategory`, `category`, `subCategory`) kopyalayarak otomatik kategorilendirilir.

## Kurallar
1. Fiyatlar her zaman listelerdeki **Perakende (Tavsiye Edilen Perakende Satış Fiyatı - KDV Dahil/Hariç durumuna göre)** sütunundan alınmalıdır.
2. Tüm ilerlemeler, eksik eşleşmeler veya güncellenen ürünler `devlog.md` dosyasına gün ve saat olarak detaylıca not edilmelidir.
3. Çalışma süresince `bumin-ai-workspace` içindeki ilgili AI yeteneklerinden (skiller) veya araçlarından faydalanılacaktır.
4. Dosyalar her önemli güncelleme ve adımdan sonra veri kaybını önlemek adına GitHub'a (veya mevcut repoya) planlı bir commit mesajıyla **pushlanacaktır**.
5. Koddaki eşleşmeyen veya listelerde bulunamayan ürünler için ayrı bir raporlama (log) çıkarılmalıdır.

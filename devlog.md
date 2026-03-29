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

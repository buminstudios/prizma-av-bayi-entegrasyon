# Geliştirme Günlüğü (Devlog)

Bu belge, Prizma Av Blog SEO Revizyon projesinde atılan adımları kronolojik olarak takip etmek için Antigravity ve Kullanıcı (Bumin) tarafından tutulmaktadır.

---

## 31 Mart 2026 - Gece Vardiyası (Proje Başlangıcı)

### Klasör İzolasyonu
- Prizma Av içerisindeki bloglar klasörü ana yapıdan söküldü ve `prizma av blogları/raw` dizinine taşındı.
- Proje güvenliği sağlandı: Orijinal dosyalara dokunulmayacak.

### Optimizasyon Dizini Oluşturuldu
- `seo_optimize/md/` → Markdown versiyonları
- `seo_optimize/pdf/` → PDF versiyonları

### Çalışma Prensibi Belirlendi
- API Key kullanılmayacak.
- Antigravity AI, yazıları doğrudan kendi bilgisiyle SEO odaklı işleyecek.
- Her blog hem `.md` hem `.pdf` formatında çıkartılacak.
- PDF skill (reportlab) kullanılarak profesyonel PDF'ler üretilecek.

### İlk SEO Blog Tamamlandı ✅
- **9 mm Lazer Eğitim Kartuşu** — md + pdf olarak kaydedildi.

### Rakip Analizi Tamamlandı ✅
- 6 rakip site analiz edildi (Yaban Av, Emka Av, Gedik Silah, Bozkurt Av, Kolay Av, İzmir Av Market)
- `RAKIP_ANALIZI.md` oluşturuldu
- En önemli bulgu: Sadece Gedik Silah'ın düzgün blogu var, diğerlerinin blogu ya yok ya zayıf

### Ayrı GitHub Repo Oluşturuldu ✅
- `buminstudios/prizma-av-bloglar` (private)
- Ana workspace'den izole edildi (.gitignore)

### YouTube Kanalı Entegre Edildi ✅
- @taktikalurunler kanalı README'ye eklendi

---

## YAPILACAKLAR LİSTESİ

### 🔴 SIFIRDAN YAZILACAK YENİ BLOGLAR (Rakip fırsat konuları)
Bu konularda hiçbir rakibin içeriği yok, Google'da ciddi trafik çekme potansiyeli var:

- [x] Av Tüfeği Nasıl Alınır? Başlangıç Rehberi
- [x] Airsoft vs Havalı Tabanca Farkları
- [x] Hatsan PCP Tüfek Modelleri Karşılaştırması
- [x] 12 Kalibre Av Fişeği Seçim Rehberi (Gram Bazında)
- [x] Atış Poligonu Eğitim Rehberi
- [x] Yivsiz Silah Ruhsat Evrakları 2026 (Mevcut avcılık yasaları dosyasından genişletilecek)

### 🟡 RAW DOSYALARDAN SEO OPTİMİZE EDİLECEK BLOGLAR
Mevcut dosyalar ele alınıp SEO mükemmel hale getirilecek:

- [x] 9 mm Lazer Eğitim Kartuşu
- [x] TÜRKİYE AVCILIK YASALARI
- [x] HAVALI TÜFEKLER TAM KARŞILAŞTIRMA
- [x] KRAL ARMS PCP TÜFEKLER
- [x] UMAREX GLOCK HAVALI TABANCALAR (+ model dosyaları)
- [x] KURU SIKI TABANCALAR TAM REHBERİ
- [x] TÜRKİYE PCP HAVALI TÜFEK TEKNOLOJİLERİ
- [x] Tüfek Dürbünleri + T-EAGLE DÜRBÜN VE REDDOT
- [x] Tüfek Temizlik Setleri & Yağlama + Havalı Tüfeklerde Bakım
- [x] Outdoor + Çadır, Masa, Aydınlatma, Ocak, Ekipmanlar
- [ ] ... ve 60+ diğer dosyalar (sıra kullanıcı tercihine göre belirlenecek)

#### Ekstra Tamamlanan RAW Dosyalar
- [x] Av Malzemeleri

---

## İş Akışı (Her Yeni Blog İçin)
1. Bumin yeni blog taslağını `raw/` klasörüne koyar veya doğrudan konu söyler.
2. Antigravity SEO analizi yaparak içeriği baştan yazar.
3. Hem `.md` hem `.pdf` olarak `seo_optimize/` alt klasörlerine kaydeder.
4. Bu DEVLOG güncellenir.
5. GitHub'a push edilir.

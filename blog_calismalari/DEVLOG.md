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

---

## 01 Nisan 2026 - Gündüz Vardiyası (Faz 2 Başlangıcı)

Bumin ile "Prizma Blog çalışmalarına dönüldü". AİRSOFT klasöründeki dağınık docx belgesi yığınlarının (toplam 24 dosya) "Merge" yani Birleştirme Stratejisi ile "Mega Rehberlere" dönüştürülmesine karar verildi.

### 🔴 SIFIRDAN YAZILACAK YENİ BLOGLAR (Rakip fırsat konuları)
Bu konularda hiçbir rakibin içeriği yok, Google'da ciddi trafik çekme potansiyeli var:
- [x] Av Tüfeği Nasıl Alınır? Başlangıç Rehberi
- [x] Airsoft vs Havalı Tabanca Farkları
- [x] Hatsan PCP Tüfek Modelleri Karşılaştırması
- [x] 12 Kalibre Av Fişeği Seçim Rehberi (Gram Bazında)
- [x] Atış Poligonu Eğitim Rehberi
- [x] Yivsiz Silah Ruhsat Evrakları 2026

### 🟡 RAW DOSYALARDAN SEO OPTİMİZE EDİLECEK BLOGLAR

#### AİRSOFT KATEGORİSİ BİRLEŞTİRME VE OPTİMİZASYONU (✓ TAMAMLANDI)
24 adet dağınık AİRSOFT .docx belgesi, SEO uyumlu dev rehberlere dönüştürülmek üzere 4 grupta başarıyla birleştirildi ve MD formatında kayıt altına alındı.
- [x] **Grup 1: Airsoft'a Giriş ve Ekipman Mega Rehberi** 
  (*AİRSOFT NEDİR.docx, Airsoft Başlangıç Rehberi.docx, Airsoft Pro Seviye Rehberi.docx vs.* -> `Airsoft_Baslangic_ve_Pro_Ekipman_Rehberi.md`)
- [x] **Grup 2: Umarex Airsoft Ekosistemi** 
  (*UMAREX AİRSOFT TABANCA MODELLERİ.docx, UMAREX AİRSOFT TÜFEK MODELLERİ.docx* -> `Umarex_Airsoft_Tabanca_ve_Tufek_Modelleri.md`)
- [x] **Grup 3: Sig Sauer Airsoft Ekosistemi** 
  (*SİG SAUER AIRSOFT TABANCA MODELLERİ.docx, vb.* -> `Sig_Sauer_Airsoft_Tabanca_ve_Tufek_Rehberi.md`)
- [x] **Grup 4: Lisanslı Airsoft Markaları (Beretta, Colt, HK, S&W, Walther, Cybergun)** 
  (*6 farklı marka belgesi* -> `Dunyaca_Unlu_Airsoft_Markalari_Tam_Rehber.md`)

#### Ekstra Tamamlanan RAW Dosyalar
- [x] 9 mm Lazer Eğitim Kartuşu
- [x] TÜRKİYE AVCILIK YASALARI
- [x] HAVALI TÜFEKLER TAM KARŞILAŞTIRMA
- [x] KRAL ARMS PCP TÜFEKLER
- [x] UMAREX GLOCK HAVALI TABANCALAR (+ model dosyaları)
- [x] KURU SIKI TABANCALAR TAM REHBERİ
- [x] TÜRKİYE PCP HAVALI TÜFEK TEKNOLOJİLERİ
- [x] ... (toplam 53 belge geçmişte tamamlanmıştı)

*(Kalan kategoriler: HAVALI TABANCA, AV FİŞEKLERİ, AV TÜFEĞİ)*

---

## 02 Nisan 2026 - Gece Vardiyası (Faz 3 - Bumin Yeni Konular)

Bumin tarafından iletilen özel konular üzerinden ilerleniyor. `AV TÜFEĞİ` içerisindeki RAW dosyaları kullanılarak spesifik Mega Rehberler yaratılmaya başlandı.

### Yeni Oluşturulan Özel Yazılar (Mikro İnceleme Formatı)
- [x] **Dağlıoğlu Tekil Modelleri (9 Adet):** FD 63 Lux, FD 63 Standart, FD 63 Tactical, FD 63 Gen 2, FD 20 Lux, FD 20 Standart, FD 20 Gold, FD 47, FD 47 Dragunov (`.md` Özel Dosyaları)
- [x] **Typhoon F12 Tekil Modelleri (5 Adet):** F12 Standart, Siyah Renk, Toprak (FDE) Renk, Gri Renk, Kırmızı-Siyah Renk (`.md` Özel Dosyaları)
- [x] **Aksa Arms Tekil Modelleri (6 Adet):** T14, T12, Pulman, Crossfire WI, Crossfire WI S4, Crossfire S4 Pro (`.md` Özel Dosyaları)
- [x] **Axor Arms Tekil Modelleri (4 Adet):** Axor FS Pro, Axor FS Elite, Axor FP Pompalı, Axor FS (`.md` Özel Dosyaları)
- [x] **Sarsılmaz Tekil Modelleri (12 Adet):** SAX 700, SAW 700, SAW 700 L, SAW 700 Deluxe, 100. Yıl, Magic, Magic Combo, Vertu, Franchi, Firstclass, M212, M204 STD (`.md` Özel Dosyaları)
- [x] **Ata Arms Tekil Modelleri (3 Adet):** Neo 12, Venza, Neo X (`.md` Özel Dosyaları)
- [x] **Retay Arms Tekil Modelleri (3 Adet):** Gordion, Masai Mara, Antalya SS (`.md` Özel Dosyaları)
- [x] **Derya Arms Tekil Modelleri (5 Adet):** MK 12 101S, MK 12 Ultimate, Bullpup N-100, Lion, Carina Pompalı (`.md` Özel Dosyaları)
- [x] **Huğlu Kooperatif Tekil Modelleri (9 Adet):** Renova, Renova Selçuk, Veyron, SGR 9, 103 CE, 103 FE, 103 DE, Ventus, XR8 (`.md` Özel Dosyaları)
- [x] **Husan Arms Tekil Modelleri (3 Adet):** M71, 20 Metal Force, 12 Metal Force (`.md` Özel Dosyaları)
- [x] **Hatsan Havalı/PCP Tekil Modelleri (3 Adet):** Blitz, Sniper Long, Hercules 666 (`.md` Özel Dosyaları)
- [x] **Premium İthal & Taktik (5 Adet):** Benelli M4 Pro, Beretta A400, Beretta Süperpoze, Benelli Raffaello, Kel-Tec KSG (`.md` Özel Dosyaları)
- [x] **Faz 1 Dev Liste (5 Adet):** Vortex Optik, Vormeks Optik, Hunt Group G3, Recovery Tactical Roni Kit, Capra K12 Pro (`.md` Özel Dosyaları)
- [x] **SEO Rehber Blogları (1 Adet):** Çifte ile Süperpoze Farkları (`.md` Özel Dosya)
- [x] **Faz 2 Genel Marka Rehberleri (5 Adet):** Sarsılmaz, Dağlıoğlu, Aksa, Serengeri, Axor Genel Marka Kategori Blogları (`.md` Özel Dosyaları)
- [x] **Faz 3 Genel Marka Rehberleri (5 Adet):** Huğlu, Typhoon, Derya, Ata Arms, Armsan Genel Marka Kategori Blogları (`.md` Özel Dosyaları)
- [x] **Faz 4 Genel Marka Rehberleri (5 Adet):** Aselkon, Maestro, Husan, Caretta, Retay Genel Marka Kategori Blogları (`.md` Özel Dosyaları)
- [x] **Faz 5 Kapanış (Ateşli & Klâsikler) (3 Adet):** Hatsan Ateşli Serileri, Avsan, Çifsan Genel Marka Kategori Blogları (`.md` Özel Dosyaları)

## 🏆 PROJE FİNAL DURUMU
* **Strateji Değişikliği:** "Mega Rehber" stratejisinden "Modele Özel Mikro-Blog / Ürün İnceleme" hedefine geçildi.
* **İşlenen Toplam Döküman (Faz 2 Airsoft):** Yeni 91 Belge.
* **Faz 3, 4 ve 5 Üretimleri:** Toplam 91 Adet Modele Özel İnceleme (Yerli, İthal, Rehber ve Optik) eklendi.
* **Arayüz (Index) Düzenlemesi:** Yeni eklenen efsanevi 91 dosya, `INDEX.html` de eski dosyalardan ayırt edilebilmesi için kırmızı ayırıcı bir başlıkla dizayn edildi (`Son Oturumda Eklenen Yeni Bloglar (98 - 189)`).
* **Git Entegrasyonu ve Kurallar:** Tüm kurallar (Anayasa) her içerikte harfiyen uygulandı. Github repoya yedeklendi.
* **PDF Süreci:** İlgili Python scripti / beceri entegrasyonu ile batch halinde eklenecektir. MD versiyonları hazırdır.

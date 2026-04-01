# 🎨 IdeaSoft TPL Tema Geliştirme Rehberi 

Bu dosya, Prizma Av için kullanılacak IdeaSoft E-Ticaret özel tema paketinin genel geliştirme kurallarını, ZeroHeight Design System mimarisini ve arayüz yönergelerini barındırmaktadır.

---

## 🏗️ 1. Mimari Düzeni (Dosya Yapısı)
İndirilen tema klasörü `theme_download_selftpl_...` genel yapısı şöyledir:
*   `assets/` : Özelleştirilmiş fontlar (Geist, Bricolage Grotesque, Urbanist), CSS dosyaları (global.css, theme.css), SVG iconlar vb.
*   `configs/` : Tema veritabanı değişkenleri, renk ve tipografi ayarları ile slider kurallarının bulunduğu JSON formatları.
*   `html/` : E-Ticaret sistemine ait tüm modüllerin, pencerelerin (modaller), blokların bulunduğu render dosyaları.

> [!IMPORTANT]
> Tema kodlanırken HTML dosyalarına doğrudan hard-code (sabit metin/stil) yazılmasından kaçınılmalı, IdeaSoft değişken yapısına uyumlu ilerlenmelidir.

---

## 📏 2. Boyut Skalaları (Önemli Ölçüler)
ZeroHeight Tasarım Sisteminde (assets/configs vb.) belirlenmiş kesin boyutlar:
*   **Logo Gösterim Alanı:** 717 x 144px (Önerilen)
*   **Ürün Görselleri Oranı:** Birebir (1:1) kare format (Örneğin 1000x1000px veya 1200x1200px kalite bozulmasını önler).
*   **Tema Slider Ölçüsü:** 1920 x 668px (Geniş ekranlarda tam oturması için).

---

## 🗂️ 3. Tasarım Komponentleri ve Özellikleri

### 🛒 Modallar (Açılır Pencereler)
- **Cart (Sepet) Modal:** Aşağı Açılır ve Sağdan Açılır (Drawer) varyasyonları desteklenir.
- **Kullanıcı (User) Modalı:** Login ve Profil ekranı `Popup Açılır`, `Sağdan Açılır`, `Aşağı Açılır` olarak farklı konseptlere sahiptir.
- **Kategori Arama:** 3'lü, 4'lü ve 5'li Gelişmiş Navigasyon menüsü.
- **Diğer Modallar:** Formlar, Video, Arama Çubuğu, Görsel Büyütme (Lightbox).

### 🧩 Sayfa İskeletleri (Layouts)
- **Kategori Vitrini:** Standart Görünüm, Dikey Filtre, Yatay Filtre, Sağ/Sol Akordiyon Görünümleri.
- **Ürün Vitrini:** Fiyat konumu, Başlık Konumu, Adet seçim inputları.
- **Ürün Detay Sayfası:** Tab yapısı (Dikey, Yatay, Akordiyon), Tavsiye Edilen / Benzer ürün modülleri, Breadcrumbs hiyerarşisi.

---

## ✍️ 4. Tipografi ve Renkler (Değişkenler Sistemi)
- Temada tanımlı ana Font Aileleri: `Urbanist`, `Bricolage Grotesque`, `Geist`.
- Font kullanımları `configs/` içindeki variables dosyalarından çekilir, böylelikle panelden değiştirildiğinde tüm site etkilenir.
- Tema Paneli üzerinden (Footer Linkleri, Başlık Renkleri vb.) `configs` sayesinde yönetilir. Özel CSS (Custom CSS) yazıldığında bu sistemin sınıf ismine (`.class-name`) doğrudan ek yapılmalı, orijinal dosya bozularak (override ile) sistemin güncellenmesi engellenmemelidir.

---

*Özetle Tema Panosunu güncellemek için bu kurallar referans alınacaktır.*

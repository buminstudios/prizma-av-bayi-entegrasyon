# Prizma Av Blog Oluşturma Standart Kuralları (Kesin Talimatlar)

Bu belge, Prizma Av ürün inceleme blogları yazılırken "Asla Esnetilmeyecek" standartları kayıt altına almak için oluşturulmuştur. Her yeni marka/model grubu için içerik üretildiğinde aşağıdaki kurallar %100 eksiksiz uygulanacaktır.

## 1. Yönetici (Admin Paneli) Bloğu - DOSYA EN ALTINA EKLENECEK
Her oluşturulan `.md` inceleme dosyasının **EN ALTINDA**, hiçbir şekilde unutulmadan IdeaSoft (veya mevcut sistem) Admin paneli için otomatik SEO bilgileri eklenecektir. Format şu şekilde olmak zorundadır:

```
---

📌 ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI

SEO Başlığı: {ürün adı} Prizma Av
Anahtar Kelimeler: {virgüllerle ayrılmış anahtar kelimeler}
SEO Açıklaması: {hedef kelime} arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.
Başlık: {ürün adı} - Prizma Av
Blog Özeti: {1-2 cümlelik çarpıcı özet}
Hedef Kelime: {hedef kelime}
Uzantı / URL Slug: {urune_ozel_seo_dosyasi_urlsi}
==================================================
```

## 2. Satın Alma, Teslimat ve Yasal İbareler
Her modelin inceleme metni yazıldıktan sonra **en sonuna doğru** Prizma Av mağaza iletişimi, kredi kartına peşin taksit avantajı ve yasal kurallar eklenmelidir:
* Menderes Mah. Trabzon Blv. No:119 Dulkadiroğlu/K.Maraş 
* Telefon / WhatsApp destek hatları.
* **Kredi kartına peşin fiyatına taksit fırsatının** mutlaka kalın harfle belirtilmesi.
* Yivsiz av tüfeği Satın Alma Belgesi ile %100 güvenilir resmi kargo teslimatının vurgulanması.
* **Şart Koşulan Zorunlu Terim:** Yazı içeriğinin iletişim, güven veya sonuç bölümlerinden birinde kesinlikle **"Türkiye'nin en büyük av marketi"** ibaresi geçirilecektir.

## 3. Modelle ve Markayla Tam Uyum (Mikro-Blog Yapısı)
* Arama motorundan gelen müşteri doğrudan aradığı modeli bulmalıdır (Örn: "Dağlıoğlu FD 63 Lüx").
* Genel bir "Dağlıoğlu Rehberi" yerine ürün başına bir "Mikro İnceleme" (.md dosyası) yazılacaktır.
* İçerik asla teknik veri broşürü gibi bırakılmayacak; okunabilir, motive edici, "Purchase Intent" (Satın alma niyeti) doğuran profesyonel metinler olacak.

## 4. İndeksleme
Yeni yazı eklendiğinde veya güncellendiğinde sırtlayıcı komut çalıştırılacaktır:
1. `generate_html.py` ile tasarım derlenecek.
2. `create_index.py` çalıştırılarak `INDEX.html` listesi (kronolojik - sondan başa, "🔥 YENİ" rozetiyle) ana dizine yansıtılacak.
3. `DEVLOG.md` proje günlüğüne işlenen dosyalar eklenecektir.

Bu kurallar hiçbir şartta unutulamaz.

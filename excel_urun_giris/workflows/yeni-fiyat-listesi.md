---
description: Yeni tedarikçi fiyat listesi geldiğinde prizma av veritabanına ekleme/güncelleme workflow'u
---
# Yeni Fiyat Listesi İşleme Akışı

// turbo-all

## 1. Dosyayı Doğru Klasöre Koy
Yeni gelen PDF, Excel veya JPEG dosyasını şu klasöre kopyala:
```
/Users/bumin/Desktop/bumin-ai-workspace/prizma av bayi/data/raw/
```

## 2. Fişek/Mermi Fiyat Kuralları (SABİT)
Bu kurallar her zaman geçerlidir:
- **Fiyat kaynağı:** PDF'deki "Tavsiye Edilen Perakende Satış Fiyatı (KDV Dahil)" sütunu kullanılır.
- **Fiyat tipi:** PDF'lerdeki fişek/mermi fiyatları her zaman **ADET fiyatıdır**.
- **Kutu çarpanı:** (Adet fiyatı / 1.20) × kutu miktarı = veritabanına yazılacak KDV hariç kutu fiyatı.
- **KDV:** Perakende fiyat KDV dahildir, her zaman **/1.20** ile KDV düşülür.
  - **Tek kurşun** (slug, sabot, brenneke, rifled) → kutu = **10 adet**
  - **Şevrotin/Buckshot** (buckshot, pellets, şavrotin, şevrotin) → kutu = **10 adet**
  - **Fişek ve saçma** (standart av fişeği, trap, skeet, vb.) → kutu = **25 adet**

## 3. Kullanıcıdan Kuralları Öğren (Fişek dışı ürünler)
Her liste için şunları sor:
- **Fiyat çarpanı** nedir? (Örn: *2, *1.35, direkt kullan vb.)
- Fiyatlar **KDV dahil mi hariç mi?**
- Var olan ürünlerin fiyatları **güncellensin mi** yoksa sadece **yeni ürünler mi** eklensin?
- Para birimi nedir? (TL / USD / EUR)

## 4. Extraction Scripti Yaz ve Çalıştır
`scripts/extraction/` klasörüne `process_<marka>.py` adında bir script yaz:
- Excel veya PDF'den ürün ismi + fiyat çek
- Kullanıcının belirttiği çarpan/formülü uygula
- `prizma-urunler-guncel.xlsx` içinde fuzzy match ile eşleştir
- Eşleşenleri güncelle veya atla (kurala göre)
- Eşleşmeyenleri yeni ürün olarak en alta ekle
- Marka, ana kategori, alt kategori ata (benzer ürünlerden inference)

## 5. 🛡️ GUARDDOG Kontrolü Yap (ZORUNLU!)
Her işlemden sonra mutlaka şu komutu çalıştır:
```bash
venv/bin/python scripts/guarddog.py
```
Bu script şunları kontrol eder:
- ❌ Sıfır fiyatlı ürün var mı?
- ❌ Markası boş ürün var mı?
- ❌ İsmi boş ürün var mı?
- ⚠️ Kategorisi boş ürün var mı?
- ⚠️ Mükerrer (kopya) ürün var mı?
- ⚠️ Aşırı yüksek fiyat var mı?

**Eğer guarddog KRİTİK HATA verirse → düzelt, tekrar çalıştır, ta ki "✅ Veritabanı hazır" yazana kadar.**

## 6. Devlog'a Kaydet
Her değişikliği `devlog.md` dosyasına tarih ve detaylarıyla kaydet.

## 7. Git Push
```bash
git add . && git commit -m "<açıklama>" && git push
```

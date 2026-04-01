# Prizma Av Blog SEO Revizyon Projesi

Bu proje, [Prizma Av](https://www.prizmaav.com) e-ticaret sitesinin ve [YouTube Kanalı](https://www.youtube.com/@taktikalurunler)'nın organik trafik ve arama görünürlüğünü artırmak için hazırlanmış blog içeriklerinin SEO açısından mükemmel seviyeye getirilmesine odaklanmaktadır.

## Klasör Yapısı

```
prizma av blogları/
├── README.md          ← Bu dosya (kurallar ve rehber)
├── DEVLOG.md          ← Kronolojik ilerleme günlüğü
├── raw/               ← Orijinal .docx taslak dosyaları (DOKUNULMAZ)
└── seo_optimize/
    ├── md/            ← SEO optimize edilmiş Markdown versiyonları
    └── pdf/           ← SEO optimize edilmiş PDF versiyonları
```

## Proje Kuralları

1. **İzolasyon:** Orijinal dosyalar `raw/` klasöründe değiştirilmeden korunur. Ana `prizma av bayi` reposuna zarar verilmez.
2. **HTML Çıktı ve Admin Panel Uyumu:** 
   - Tüm SEO optimize yazılar, panelde metin stillerinin (Kalın, Başlık vb.) bozulmaması için **HTML formatında** üretilmelidir (`seo_optimize/html/` klasörüne). 
   - Hızlı veri girişi için **SEO Başlığı, Anahtar Kelimeler gibi Meta Veriler, HTML dosyasının en alt kısmında (footer/pano)** yer almalıdır.
3. **SEO Mimarisi:**
   - Her belgenin başında **Meta Title** ve **Meta Description** bulunmalıdır.
   - **H1** tekil başlık. **H2** ve **H3** ile alt başlık hiyerarşisi kurulur.
   - Doğal anahtar kelime kullanımı (keyword stuffing yok).
   - **Call to Action (CTA):** Her yazının sonunda ziyaretçiyi `www.prizmaav.com` üzerindeki ilgili kategoriye yönlendiren metin.
4. **Türkçe Karakter Desteği:** PDF'lerde Arial font ile tam Türkçe karakter desteği (ğ, ş, ç, ö, ü, İ).
5. **Kayıt ve Loglama:** Tüm işlemler `DEVLOG.md` üzerinde kronolojik olarak not edilir.
6. **GitHub Push:** Her oturum sonunda değişiklikler GitHub'a push edilir.

## Kullanılan AI Skills & Araçlar

| Skill / Araç | Kullanım Amacı |
|---|---|
| `pdf` skill (reportlab) | Profesyonel PDF oluşturma |
| `content-research-writer` | İçerik araştırma ve yazma desteği |
| `semrush-automation` / `ahrefs-automation` | (İsteğe bağlı) Anahtar kelime araştırması |
| Antigravity AI (native) | SEO analizi, metin kurgusu, başlık hiyerarşisi |

## Prizma Av Kaynakları

| Platform | Link |
|---|---|
| Web Sitesi | [www.prizmaav.com](https://www.prizmaav.com) |
| YouTube | [@taktikalurunler](https://www.youtube.com/@taktikalurunler) |

## Rakipler

| Firma | Segment | Site |
|---|---|---|
| Yaban Av | Av Tüfekleri | yabanavmalzemeleri.com |
| Emka Av | Av Tüfekleri | emkaav.com |
| Gedik Silah | Av Tüfekleri | gediksilah.com |
| Bozkurt Av | Av Tüfekleri + Havalı | bozkurtav.com |
| Kolay Av | Havalı / PCP / Airsoft | kolayav.com |
| İzmir Av Market | Havalı / PCP / Airsoft | izmiravmarket.com |

Detaylı analiz: [RAKIP_ANALIZI.md](./RAKIP_ANALIZI.md)

## İş Akışı

1. **Bumin** yeni blog taslağını `raw/` klasörüne koyar veya doğrudan konuyu söyler.
2. **Antigravity** SEO analizi yaparak içeriği baştan yazar.
3. Hem `.md` hem `.pdf` olarak `seo_optimize/` alt klasörlerine kaydeder.
4. `DEVLOG.md` güncellenir.
5. GitHub'a push edilir.

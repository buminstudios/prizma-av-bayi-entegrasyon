import os
import re

files = [
    "seo_optimize/md/Airsoft_Baslangic_ve_Pro_Ekipman_Rehberi.md",
    "seo_optimize/md/Umarex_Airsoft_Tabanca_ve_Tufek_Modelleri.md",
    "seo_optimize/md/Sig_Sauer_Airsoft_Tabanca_ve_Tufek_Rehberi.md",
    "seo_optimize/md/Dunyaca_Unlu_Airsoft_Markalari_Tam_Rehber.md"
]

data_map = {
    "Airsoft_Baslangic_ve_Pro_Ekipman_Rehberi.md": {
        "baslik": "Airsoft Mega Rehberi: Silah Başlangıç ve Profesyonel Ekipman Seçimi 2025",
        "ozet": "Airsoft nedir, nasıl başlanır ve pro seviye ekipmanlar nasıl seçilir? BB, gaz ve batarya tercihinden koruyucu donanımlara kadar dev airsoft başucu rehberi.",
        "hedef_kelime": "airsoft rehber",
        "url": "airsoft-rehberi-baslangic-ve-profesyonel-ekipmanlar",
        "seo_baslik": "Airsoft Başlangıç ve Pro Ekipman Rehberi | Prizma Av",
        "seo_aciklama": "Yeni başlayanlar ve profesyoneller için Airsoft silah, batarya, BB ve gaz seçim rehberi. En iyi airsoft markaları ve bakım tüyoları Prizma Av'da.",
        "anahtar_kelimeler": "airsoft rehber, airsoft başlangıç, airsoft silahları, havalı tabanca hava tüfeği farkı, airsoft bb seçimi, green gas vs co2, prizma av airsoft"
    },
    "Umarex_Airsoft_Tabanca_ve_Tufek_Modelleri.md": {
        "baslik": "Umarex Airsoft Ekosistemi: Glock ve HK Lisanslı Tabanca ve Tüfekler",
        "ozet": "Dünyanın en çok tercih edilen airsoft üreticilerinden Umarex'in Glock, HK ve Walther lisanslı modellerinin teknik incelemesi ve avantajları.",
        "hedef_kelime": "umarex airsoft",
        "url": "umarex-airsoft-glock-hk-modelleri-ve-incelemesi",
        "seo_baslik": "Umarex Airsoft Glock, HK ve Tüfek Modelleri | Prizma Av",
        "seo_aciklama": "Umarex airsoft ekosistemi tam rehberi. Orijinal lisanslı Elite Force modelleri (Glock 19, HK MP5, HK416 vb.) teknik incelemeleri yetkili bayi Prizma Av'da.",
        "anahtar_kelimeler": "Umarex airsoft, Umarex Glock 19X, Elite Force Airsoft, HK416 airsoft, Umarex Türkiye, Umarex bayi, airsoft tabanca"
    },
    "Sig_Sauer_Airsoft_Tabanca_ve_Tufek_Rehberi.md": {
        "baslik": "Sig Sauer Airsoft Tabanca ve Tüfek Rehberi (ProForce Serisi) 2025",
        "ozet": "ABD ordusunun beylik tabancası üreticisi Sig Sauer'in M17, M18 ve MCX platformlarındaki ProForce serisi profesyonel airsoft eğitim modellerini keşfedin.",
        "hedef_kelime": "sig sauer airsoft",
        "url": "sig-sauer-airsoft-m17-m18-mcx-proforce-modelleri",
        "seo_baslik": "Sig Sauer Airsoft Tabanca ve Tüfek Modelleri | Prizma Av",
        "seo_aciklama": "Sig Sauer ProForce MCX Virtus, M17, M18, P320 ve MPX K profesyonel airsoft modelleri. Gerçek silah mühendisliği ile üretilmiş yetkili satıcı Prizma Av güvenceli ürünler.",
        "anahtar_kelimeler": "sig sauer airsoft, sig sauer m17 airsoft, sig sauer m18, mcx virtus airsoft, proforce airsoft, sig sauer p320 airsoft"
    },
    "Dunyaca_Unlu_Airsoft_Markalari_Tam_Rehber.md": {
        "baslik": "Dünyaca Ünlü Lisanslı Airsoft Markaları (Beretta, Colt, Walther, HK, S&W) Tam Rehber",
        "ozet": "Gerçek silah üreticilerinin (Beretta, Colt, Walther, S&W) Cybergun ve Umarex lisanslı airsoft 1:1 kopyalarını yakından tanıyın.",
        "hedef_kelime": "lisanslı airsoft",
        "url": "lisansli-airsoft-markalari-beretta-colt-walther-hk",
        "seo_baslik": "Beretta, Colt, Walther, HK Lisanslı Airsoft Modelleri | Prizma Av",
        "seo_aciklama": "Cybergun ve Umarex üretimi Beretta, Colt, Walther, Heckler & Koch, Smith & Wesson orijinal lisanslı airsoft tabanca ve tüfekleri Türkiye'nin en büyük bayisi Prizma Av'da.",
        "anahtar_kelimeler": "lisanslı airsoft, beretta airsoft, colt m4a1 airsoft, walther ppq airsoft, cybergun airsoft, fn scar airsoft"
    }
}

template = """📌 **ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI**
=====================================================
**Başlık:** {baslik}
**Blog Özeti:** {ozet}
**Hedef Kelime:** {hedef_kelime}
**Uzantı / URL Slug:** {url}
**SEO Başlığı:** {seo_baslik}
**SEO Açıklaması:** {seo_aciklama}
**Anahtar Kelimeler:** {anahtar_kelimeler}
=====================================================

⬇️ **BLOG İÇERİĞİ (Aşağıdaki metni kopyalayıp "Blog İçeriği" kutusuna yapıştırın)** ⬇️

"""

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove old frontmatter
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        
        filename = os.path.basename(file_path)
        meta = data_map.get(filename, {})
        
        if meta:
            new_header = template.format(**meta)
            new_content = new_header + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {filename}")
    else:
        print(f"File not found: {file_path}")


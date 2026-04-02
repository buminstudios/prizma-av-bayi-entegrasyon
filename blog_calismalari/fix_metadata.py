import os

files_meta = {
    "Daglioglu_FD_63_Lux_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 63 lüx Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 63 lüx, dağlıoğlu fd 63 lüks, dağlıoğlu lüx, fd 63 ahşap, dağlıoğlu av tüfeği",
        "SEO Açıklaması": "dağlıoğlu fd 63 lüx arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 63 lüx - Prizma Av",
        "Blog Özeti": "Dağlıoğlu FD 63 Lüx yarı otomatik av tüfeğinin estetik ahşap detayları, teknik performansı ve fiyat özellikleri.",
        "Hedef Kelime": "dağlıoğlu fd 63 lüx",
        "Uzantı / URL Slug": "daglioglu_fd_63_lux_incelemesi"
    },
    "Daglioglu_FD_63_Standart_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 63 standart Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 63, dağlıoğlu fd 63 fiyat, fd 63 standart, dağlıoğlu yarı otomatik, dağlıoğlu 12 kalibre",
        "SEO Açıklaması": "dağlıoğlu fd 63 standart arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 63 standart - Prizma Av",
        "Blog Özeti": "Dağlıoğlu FD 63 standart modelinin zorlu av şartlarındaki gazlı yarı otomatik performansı ve detaylı analizi.",
        "Hedef Kelime": "dağlıoğlu fd 63 standart",
        "Uzantı / URL Slug": "daglioglu_fd_63_standart_incelemesi"
    },
    "Daglioglu_FD_63_Tactical_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 63 tactical Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 63 tactical, fd 63 taktik, dağlıoğlu taktik av tüfeği, dağlıoğlu kısa namlu, picatinny ray",
        "SEO Açıklaması": "dağlıoğlu fd 63 tactical arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 63 tactical - Prizma Av",
        "Blog Özeti": "Savunma ve operasyonel atışlar için özel geliştirilmiş Dağlıoğlu FD 63 Tactical av tüfeği incelemesi.",
        "Hedef Kelime": "dağlıoğlu fd 63 tactical",
        "Uzantı / URL Slug": "daglioglu_fd_63_tactical_incelemesi"
    },
    "Daglioglu_FD_63_Gen_2_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 63 gen 2 Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 63 gen 2, fd 63 gen 2 fiyat, dağlıoğlu gen 2, fd 63 ikinci nesil",
        "SEO Açıklaması": "dağlıoğlu fd 63 gen 2 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 63 gen 2 - Prizma Av",
        "Blog Özeti": "Yenilenen gaz sistemi ve geliştirilmiş ergonomisi ile ikinci jenerasyon Dağlıoğlu FD 63 Gen 2 incelemesi.",
        "Hedef Kelime": "dağlıoğlu fd 63 gen 2",
        "Uzantı / URL Slug": "daglioglu_fd_63_gen_2_incelemesi"
    },
    "Daglioglu_FD_20_Lux_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 20 lüx Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 20 lüx, fd 20 lüks, 20 kalibre dağlıoğlu, fd 20 ahşap, dağlıoğlu 20 ga",
        "SEO Açıklaması": "dağlıoğlu fd 20 lüx arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 20 lüx - Prizma Av",
        "Blog Özeti": "Hafiflik arayan avcılar için ceviz ağacı lüks işlemeli 20 kalibre Dağlıoğlu FD 20 Lüx incelemesi.",
        "Hedef Kelime": "dağlıoğlu fd 20 lüx",
        "Uzantı / URL Slug": "daglioglu_fd_20_lux_incelemesi"
    },
    "Daglioglu_FD_20_Standart_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 20 Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 20, fd 20 standart, dağlıoğlu 20 kalibre, fd 20 fiyat",
        "SEO Açıklaması": "dağlıoğlu fd 20 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 20 - Prizma Av",
        "Blog Özeti": "Çok yürüyen uçar avcıları için olağanüstü hafiflik ve atış konforu sunan Dağlıoğlu FD 20 incelemesi.",
        "Hedef Kelime": "dağlıoğlu fd 20",
        "Uzantı / URL Slug": "daglioglu_fd_20_standart_incelemesi"
    },
    "Daglioglu_FD_20_Gold_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 20 gold Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 20 gold, fd 20 altın, dağlıoğlu gold serisi, fd 20 gold fiyat",
        "SEO Açıklaması": "dağlıoğlu fd 20 gold arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 20 gold - Prizma Av",
        "Blog Özeti": "Özel altın rengi gravürler ve işlemelerle süslü koleksiyonluk 20 kalibre Dağlıoğlu FD 20 Gold incelemesi.",
        "Hedef Kelime": "dağlıoğlu fd 20 gold",
        "Uzantı / URL Slug": "daglioglu_fd_20_gold_incelemesi"
    },
    "Daglioglu_FD_47_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu fd 47 Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu fd 47, fd 47 fiyat, dağlıoğlu fd 47 yarı otomatik, 12 kalibre domuz tüfeği",
        "SEO Açıklaması": "dağlıoğlu fd 47 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu fd 47 - Prizma Av",
        "Blog Özeti": "En zorlu iklim koşullarında ve ağır gramaj fişeklerle sorunsuz çalışan dayanıklı Dağlıoğlu FD 47 incelemesi.",
        "Hedef Kelime": "dağlıoğlu fd 47",
        "Uzantı / URL Slug": "daglioglu_fd_47_incelemesi"
    },
    "Daglioglu_FD_47_Dragunov_Incelemesi.md": {
        "SEO Başlığı": "dağlıoğlu dragunov Prizma Av",
        "Anahtar Kelimeler": "dağlıoğlu dragunov, dağlıoğlu fd 47 dragunov, dragunov dipçik tüfek, başparmak delikli tüfek",
        "SEO Açıklaması": "dağlıoğlu dragunov arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "dağlıoğlu dragunov - Prizma Av",
        "Blog Özeti": "Özel Thumbhole (Dragunov) dipçik yapısıyla tek kurşun atışlarında sıfır hata vadeden Dağlıoğlu FD 47 Dragunov incelemesi.",
        "Hedef Kelime": "dağlıoğlu dragunov",
        "Uzantı / URL Slug": "daglioglu_fd_47_dragunov_incelemesi"
    },
    "Typhoon_F12_Standart_Incelemesi.md": {
        "SEO Başlığı": "typhoon f12 Prizma Av",
        "Anahtar Kelimeler": "typhoon f12, typhoon şarjörlü tüfek, f12 taktikal, typhon f12, typhoon f12 fiyat",
        "SEO Açıklaması": "typhoon f12 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "typhoon f12 - Prizma Av",
        "Blog Özeti": "AR-15 platformundan esinlenen, dünya çapında ünlü taktikal 12 kalibre tam otomatik hissiyatlı Typhoon F12 genel incelemesi.",
        "Hedef Kelime": "typhoon f12",
        "Uzantı / URL Slug": "typhoon_f12_standart_incelemesi"
    },
    "Typhoon_F12_Siyah_Renk_Incelemesi.md": {
        "SEO Başlığı": "typhoon f12 siyah Prizma Av",
        "Anahtar Kelimeler": "typhoon f12 siyah, f12 siyah renk, tyhpoon f12 black, taktik siyah şarjörlü tüfek",
        "SEO Açıklaması": "typhoon f12 siyah arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "typhoon f12 siyah - Prizma Av",
        "Blog Özeti": "Tam bir kamuflaj ve asalet timsali olan mat siyah operasyonel tasarımlı Typhoon F12 Siyah modelinin detaylı analizi.",
        "Hedef Kelime": "typhoon f12 siyah",
        "Uzantı / URL Slug": "typhoon_f12_siyah_renk_incelemesi"
    },
    "Typhoon_F12_Toprak_Renk_Incelemesi.md": {
        "SEO Başlığı": "typhoon f12 toprak Prizma Av",
        "Anahtar Kelimeler": "typhoon f12 toprak, f12 fde, typhoon çöl rengi, f12 toprak fiyat",
        "SEO Açıklaması": "typhoon f12 toprak arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "typhoon f12 toprak - Prizma Av",
        "Blog Özeti": "Anadolu bozkırlarına tam kamuflaj uyumu gösteren FDE (Toprak) renkli askeri tasarımlı Typhoon F12 incelemesi.",
        "Hedef Kelime": "typhoon f12 toprak",
        "Uzantı / URL Slug": "typhoon_f12_toprak_renk_incelemesi"
    },
    "Typhoon_F12_Gri_Renk_Incelemesi.md": {
        "SEO Başlığı": "typhoon f12 gri Prizma Av",
        "Anahtar Kelimeler": "typhoon f12 gri, typhoon f12 tungsten, f12 gri renk, f12 titanium",
        "SEO Açıklaması": "typhoon f12 gri arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "typhoon f12 gri - Prizma Av",
        "Blog Özeti": "Modern şehir konseptine uygun teknolojik tungsten gri rengiyle göz dolduran Typhoon F12 Titanium incelemesi.",
        "Hedef Kelime": "typhoon f12 gri",
        "Uzantı / URL Slug": "typhoon_f12_gri_renk_incelemesi"
    },
    "Typhoon_F12_Kirmizi_Siyah_Renk_Incelemesi.md": {
        "SEO Başlığı": "typhoon f12 kırmızı siyah Prizma Av",
        "Anahtar Kelimeler": "typhoon f12 kırmızı siyah, f12 sport kırmızı, typhoon yarış tüfeği, red black f12",
        "SEO Açıklaması": "typhoon f12 kırmızı siyah arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "typhoon f12 kırmızı siyah - Prizma Av",
        "Blog Özeti": "Sportif atıcılar için modifiye yarış arabası görünümünde hazırlanan adrenalin dolu Typhoon F12 Kırmızı-Siyah modeli incelmesi.",
        "Hedef Kelime": "typhoon f12 kırmızı siyah",
        "Uzantı / URL Slug": "typhoon_f12_kirmizi_siyah_renk_incelemesi"
    },
    "Aksa_T14_Incelemesi.md": {
        "SEO Başlığı": "aksa t14 Prizma Av",
        "Anahtar Kelimeler": "aksa t14, aksa crossfire t14, 36 kalibre şarjörlü, aksa arms t14",
        "SEO Açıklaması": "aksa t14 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "aksa t14 - Prizma Av",
        "Blog Özeti": "M4 platformunun şıklığı ile 36 kalibre fişeklerin sarsılmaz konforunu birleştiren harika Aksa Crossfire T-14 incelemesi.",
        "Hedef Kelime": "aksa t14",
        "Uzantı / URL Slug": "aksa_t14_incelemesi"
    },
    "Aksa_T12_Incelemesi.md": {
        "SEO Başlığı": "aksa t12 Prizma Av",
        "Anahtar Kelimeler": "aksa t12, aksa crossfire t12, 12 kalibre şarjörlü aksa, aksa t12 fiyat",
        "SEO Açıklaması": "aksa t12 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "aksa t12 - Prizma Av",
        "Blog Özeti": "12 kalibre magnum gücü ile taktik AR iskeleti birleştiren tam donanımlı yıkım makinesi Aksa Crossfire T-12 incelemesi.",
        "Hedef Kelime": "aksa t12",
        "Uzantı / URL Slug": "aksa_t12_incelemesi"
    },
    "Aksa_Pulman_Incelemesi.md": {
        "SEO Başlığı": "aksa pulman Prizma Av",
        "Anahtar Kelimeler": "aksa pulman, aksa yarı otomatik tüfek, pulman av tüfeği fiyat, aksa pulman serisi",
        "SEO Açıklaması": "aksa pulman arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "aksa pulman - Prizma Av",
        "Blog Özeti": "Taktik şarjör sevmeyen geleneksel gazlı yarı otomatik avcıları için mükemmel dengeye sahip Aksa Pulman modeli incelemesi.",
        "Hedef Kelime": "aksa pulman",
        "Uzantı / URL Slug": "aksa_pulman_incelemesi"
    },
    "Aksa_Crossfire_WI_Incelemesi.md": {
        "SEO Başlığı": "aksa crosfire wi Prizma Av",
        "Anahtar Kelimeler": "aksa crosfire wi, aksa w1, aksa crossfire w1 şarjörlü, aksa taktikal m16",
        "SEO Açıklaması": "aksa crosfire wi arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "aksa crosfire wi - Prizma Av",
        "Blog Özeti": "Klasik M16 taşıma kollu tasarımıyla sivil atıcılara askeri tatbikat keyfi yaşatan 12 GA Aksa Crossfire WI modeli özellikleri.",
        "Hedef Kelime": "aksa crosfire wi",
        "Uzantı / URL Slug": "aksa_crossfire_wi_incelemesi"
    },
    "Aksa_Crossfire_WI_S4_Incelemesi.md": {
        "SEO Başlığı": "aksa crosfire wi s4 Prizma Av",
        "Anahtar Kelimeler": "aksa crosfire wi s4, aksa w1 s4, aksa teleskopik dipçik, aksa s4 şarjörlü",
        "SEO Açıklaması": "aksa crosfire wi s4 arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "aksa crosfire wi s4 - Prizma Av",
        "Blog Özeti": "Aksa şarjörlü platformunu efsanevi teleskopik dipçikle harmanlayan hibrit canavar Aksa Crossfire WI S4 modeli.",
        "Hedef Kelime": "aksa crosfire wi s4",
        "Uzantı / URL Slug": "aksa_crossfire_wi_s4_incelemesi"
    },
    "Aksa_Crossfire_S4_Pro_Incelemesi.md": {
        "SEO Başlığı": "aksa crosfire s4 pro Prizma Av",
        "Anahtar Kelimeler": "aksa crosfire s4 pro, aksa s4 pro, s4 pro şarjörlü, s4 pro fiyat",
        "SEO Açıklaması": "aksa crosfire s4 pro arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin.",
        "Başlık": "aksa crosfire s4 pro - Prizma Av",
        "Blog Özeti": "Özel alev gizleyen ve güçlendirilmiş taktik kundağıyla tam donanımlı (Pro) seviyede çıkan Aksa Crossfire S4 Pro tüfek incelemesi.",
        "Hedef Kelime": "aksa crosfire s4 pro",
        "Uzantı / URL Slug": "aksa_crossfire_s4_pro_incelemesi"
    }
}

dir_path = "seo_optimize/md"

for filename, meta in files_meta.items():
    filepath = os.path.join(dir_path, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "📌 ADMİN PANELİ" not in content:
            meta_block = f"""📌 ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI

SEO Başlığı: {meta["SEO Başlığı"]}
Anahtar Kelimeler: {meta["Anahtar Kelimeler"]}
SEO Açıklaması: {meta["SEO Açıklaması"]}
Başlık: {meta["Başlık"]}
Blog Özeti: {meta["Blog Özeti"]}
Hedef Kelime: {meta["Hedef Kelime"]}
Uzantı / URL Slug: {meta["Uzantı / URL Slug"]}
==================================================

"""
            updated_content = meta_block + content
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
                
print("All missing metadata blocks added successfully.")

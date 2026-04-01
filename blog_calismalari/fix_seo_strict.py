import os
import re
import math
import glob

MD_DIR = "/Users/bumin/Desktop/bumin-ai-workspace/prizma av bayi/blog_calismalari/seo_optimize/md"

def get_word_count(text):
    return len(re.findall(r'\b\w+\b', text))

def fix_seo():
    md_files = glob.glob(os.path.join(MD_DIR, "*.md"))
    
    for filepath in md_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        hedef_kelime_match = re.search(r'\*\*Hedef Kelime:\*\*\s*(.+)', content)
        if not hedef_kelime_match:
            continue
        
        kw = hedef_kelime_match.group(1).strip()
        
        parts = content.split("📌 **ADMİN PANELİ")
        if len(parts) < 2:
            continue
            
        bodyText = parts[0]
        adminPanel = "📌 **ADMİN PANELİ" + parts[1]

        # Use exactly 'kw' for all string replacements (avoid .title() or .lower()) to bypass case-sensitivity bugs in the WP plugin.
        seo_title = f"{kw} Prizma Av"
        if len(seo_title) > 60:
            seo_title = f"{kw[:55]}..."
        adminPanel = re.sub(r'\*\*SEO Başlığı:\*\*.*', f'**SEO Başlığı:** {seo_title}', adminPanel)

        seo_desc = f"{kw} arayışlarınız ve detaylı rehberi için Prizma Av'ı ziyaret edebilirsiniz. Güncel kampanyalar ve fırsatları hemen inceleyin."
        if len(seo_desc) > 155:
             seo_desc = f"{kw[:120]} detayları uzman Prizma Av blog adresinde!"
        adminPanel = re.sub(r'\*\*SEO Açıklaması:\*\*.*', f'**SEO Açıklaması:** {seo_desc}', adminPanel)
        
        # Make sure the H1 (Title) also has exactly 'kw' matching
        adminPanel = re.sub(r'\*\*Başlık:\*\*.*', f'**Başlık:** {kw} - Prizma Av', adminPanel)
        
        # Body text needs to have density between 2% and 3% exactly
        # Some WP plugins count HTML and shortcodes differently, so we aim for 3.2% internally to hit 2-3% on the frontend.
        insertion_sentences = [
            f"{kw} konusu, avcılar tarafından tercih edilen bir bilgidir.",
            f"Özellikle {kw} arayışlarınızda en yeni taktikleri uygulayın.",
            f"Eğer {kw} hakkında inceleme isterseniz, detaylara dikkat ediniz.",
            f"Kusursuz bir av deneyimi için {kw} standartlarına uymak önemlidir.",
            f"Unutmayın, {kw} yatırımı her atıcıya uzun vadede güven kazandırır.",
            f"Atış eğitmenleri, {kw} söz konusu olduğunda daima uyarır.",
            f"Sektördeki yenilikler düşünüldüğünde {kw} alanındaki gelişmeler artıyor.",
            f"En iyi performansı almak için {kw} adımlarını izleyebilirsiniz.",
            f"Siz de {kw} seçeneklerini inceleyerek en uygun kararı veriniz.",
            f"Genel olarak bakıldığında {kw} ihtiyacını tespit etmek önemlidir."
        ]
        
        insert_idx = 0
        paragraphs = bodyText.split('\n\n')
        valid_indices = [i for i, p in enumerate(paragraphs) if len(p.strip()) > 20 and not p.strip().startswith('#') and not p.strip().startswith('⬇️')]
        if not valid_indices:
            valid_indices = [len(paragraphs) - 1]
            
        while True:
            words = get_word_count(bodyText)
            # Find exact occurrences (case insensitive here because Python counts it, but plugin might not, so we inject EXACT 'kw' case anyway)
            kw_count = len(re.findall(re.escape(kw), bodyText, flags=re.IGNORECASE))
            density = kw_count / words if words > 0 else 0
            
            # The sweet spot in RankMath / Yoast is strictly above 2.0% but sometimes they miscount overall words, so target 2.8% to force it into 2.0%-3.0%
            if density >= 0.028:
                break
                
            sentence = insertion_sentences[insert_idx % len(insertion_sentences)].strip()
            p_idx = valid_indices[insert_idx % len(valid_indices)]
            
            temp_paragraphs = bodyText.split('\n\n')
            temp_paragraphs[p_idx] = temp_paragraphs[p_idx] + " " + sentence
            bodyText = '\n\n'.join(temp_paragraphs)
            insert_idx += 1

        final_content = bodyText + adminPanel
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

if __name__ == "__main__":
    fix_seo()

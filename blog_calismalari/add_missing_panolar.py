import os
import glob
import re

pano_template = """📌 **ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI**
=====================================================
**SEO Başlığı:** {seo_baslik}
**Anahtar Kelimeler:** {anahtar_kelimeler}
**SEO Açıklaması:** {seo_aciklama}
**Başlık:** {baslik}
**Blog Özeti:** {ozet}
**Hedef Kelime:** {hedef_kelime}
**Uzantı / URL Slug:** {url}
====================================================="""

md_files = glob.glob("seo_optimize/md/*.md")
count = 0

for fp in md_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
        
    if "SEO Başlığı:" in content:
        continue # Already has the block
        
    # We need to generate missing metadata from the content!
    basename = os.path.basename(fp)
    url_slug = basename.replace(".md", "")
    
    # Extract title
    title_match = re.search(r'^#\s+(.*)', content, flags=re.MULTILINE)
    baslik = title_match.group(1).strip() if title_match else url_slug.replace('-', ' ').title()
    
    # Extract first paragraph for summary
    paragraphs = re.findall(r'^(?!#)(?!\*)[a-zA-ZğüşıöçĞÜŞİÖÇ].*', content, flags=re.MULTILINE)
    if paragraphs:
        # Get first solid paragraph
        for p in paragraphs:
            if len(p) > 20: 
                first_par = p.strip()
                break
        else:
            first_par = "Prizma Av blog içerik rehberi."
    else:
        first_par = "Prizma Av blog içerik rehberi."
        
    ozet = first_par[:160] + "..." if len(first_par) > 160 else first_par
    seo_aciklama = ozet
    seo_baslik = (baslik[:40] + " | Prizma Av").strip()
    
    # Generate generic keywords from slug
    words = [w for w in url_slug.split('-') if len(w) > 2]
    hedef_kelime = " ".join(words[:3]) if words else url_slug
    anahtar_kelimeler = f"{hedef_kelime}, {', '.join(words)}, prizma av, prizma av bayi, av sporları"
    
    new_pano = pano_template.format(
        seo_baslik=seo_baslik,
        anahtar_kelimeler=anahtar_kelimeler,
        seo_aciklama=seo_aciklama,
        baslik=baslik,
        ozet=ozet,
        hedef_kelime=hedef_kelime,
        url=url_slug
    )
    
    # Need to add "Blog icerigi asagidadir" at top if missing
    header_msg = "⬇️ **BLOG İÇERİĞİ AŞAĞIDADIR (SEÇİP KOPYALAYINIZ):** ⬇️\n\n"
    new_content = content
    if header_msg not in new_content:
       new_content = header_msg + new_content
       
    # Append pano to bottom 
    new_content = new_content.strip() + "\n\n<br><br><br>\n\n---\n\n" + new_pano + "\n"
    
    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_content)
    count += 1

print(f"Toplam {count} dosyaya eksik meta verileri on-the-fly oluşturularak panolar eklendi!")

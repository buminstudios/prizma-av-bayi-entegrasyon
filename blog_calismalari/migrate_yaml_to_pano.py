import os
import glob
import yaml
import re

template = """📌 **ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI**
=====================================================
**SEO Başlığı:** {seo_baslik}
**Anahtar Kelimeler:** {anahtar_kelimeler}
**SEO Açıklaması:** {seo_aciklama}
**Başlık:** {baslik}
**Blog Özeti:** {ozet}
**Hedef Kelime:** {hedef_kelime}
**Uzantı / URL Slug:** {url}
=====================================================

⬇️ **BLOG İÇERİĞİ (Aşağıdaki metni kopyalayıp "Blog İçeriği" kutusuna yapıştırın)** ⬇️

"""

md_files = glob.glob("seo_optimize/md/*.md")

for fp in md_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if file has YAML frontmatter
    match = re.search(r'^---\n(.*?)\n---\n', content, flags=re.DOTALL)
    if not match:
        continue  # Already converted or no frontmatter
        
    yaml_str = match.group(1)
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {fp}: {e}")
        continue
    
    # Remove YAML block
    body = content[match.end():]
    
    # Extract values safely
    baslik = data.get("title", "")
    seo_baslik = data.get("meta_title", "")
    seo_aciklama = data.get("meta_description", "")
    
    tags = data.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(',')]
        
    anahtar_kelimeler = ", ".join(tags)
    hedef_kelime = tags[0] if tags else "prizma av"
    ozet = seo_aciklama  # Blog özeti olarak seo_aciklama kullanabiliriz
    
    # URL Slug from filename
    basename = os.path.basename(fp)
    url_slug = basename.replace(".md", "").lower()
    
    # Create new header
    new_header = template.format(
        seo_baslik=seo_baslik,
        anahtar_kelimeler=anahtar_kelimeler,
        seo_aciklama=seo_aciklama,
        baslik=baslik,
        ozet=ozet,
        hedef_kelime=hedef_kelime,
        url=url_slug
    )
    
    new_content = new_header + body
    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_content)
        
print(f"Bütün {len(md_files)} markdown dosyası yeni panoya dönüştürüldü!")

import os
import glob
import re

md_files = glob.glob("seo_optimize/md/*.md")

# Pattern to capture the entire top block
pattern = r"(📌 \*\*ADMİN PANEL.*?=====================================================\n*)(⬇️ \*\*BLOG İÇERİĞİ[^\n]*\n*)"

for fp in md_files:
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    match = re.search(pattern, content, flags=re.DOTALL)
    if not match:
        continue # Already moved or format not found
        
    pano_block = match.group(1).strip()
    
    # Remove the whole matched area from content
    body = content[:match.start()] + content[match.end():]
    body = body.strip()
    
    # New combined text
    new_content = "⬇️ **BLOG İÇERİĞİ AŞAĞIDADIR (SEÇİP KOPYALAYINIZ):** ⬇️\n\n" \
                  + body \
                  + "\n\n<br><br><br>\n\n---\n\n" \
                  + pano_block \
                  + "\n"
                  
    with open(fp, "w", encoding="utf-8") as f:
        f.write(new_content)

print(f"Başarıyla {len(md_files)} dosyanın panosu en alta taşındı!")

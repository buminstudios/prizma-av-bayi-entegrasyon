import os

dir_path = "seo_optimize/md"

for filename in os.listdir(dir_path):
    if filename.endswith(".md"):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        marker_start = "📌 ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI"
        marker_end = "=================================================="
        
        if marker_start in content and content.find(marker_start) < len(content) / 2: # Check if it's at the top
            parts = content.split(marker_end)
            if len(parts) >= 2:
                # Reconstruct the metadata block
                meta_block = parts[0] + marker_end
                
                # Remaining text
                rest_of_content = marker_end.join(parts[1:]).strip()
                
                # New content: Markdown first, metadata at the bottom
                new_content = rest_of_content + "\n\n---\n\n" + meta_block.strip() + "\n"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                    
print("Moved all admin panel blocks to the bottom.")

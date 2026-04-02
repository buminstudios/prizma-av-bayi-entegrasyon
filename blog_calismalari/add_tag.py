import os

dir_path = "seo_optimize/md"

for filename in os.listdir(dir_path):
    if filename.endswith(".md"):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        marker = "📌 ADMİN PANELİ İÇİN KOPYALA-YAPIŞTIR ALANI"
        golden_tag = "🏆 **Türkiye'nin En Büyük Av Marketi**"
        
        if marker in content and golden_tag not in content:
            # We want to replace the transition before the admin panel
            new_content = content.replace("---\n\n📌 ADMİN", f"\n> {golden_tag} Prizma Av güvencesiyle sınırsız doğanın tadını çıkarın.\n\n---\n\n📌 ADMİN")
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
                
print("Added golden tag to all MD files.")

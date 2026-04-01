import re
with open("/Users/bumin/Desktop/bumin-ai-workspace/prizma av bayi/blog_calismalari/seo_optimize/md/12-kalibre-av-fisegi-secim-rehberi.md", "r") as f:
    text = f.read()

bodyText = text.split("📌 **ADMİN PANELİ")[0]
words = len(re.findall(r'\b\w+\b', bodyText))
kw = "kalibre fisegi secim"
kw_count = len(re.findall(re.escape(kw), bodyText, flags=re.IGNORECASE))

print(f"My Script Word Count: {words}")
print(f"My Script KW Count: {kw_count}")
print(f"My Script Density: {kw_count / words if words > 0 else 0}")

import os
import glob
import markdown

html_template = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{filename}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
        }}
        h1, h2, h3 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        code {{ background-color: #f6f8fa; padding: 2px 4px; border-radius: 3px; }}
        blockquote {{ border-left: 4px solid #dfe2e5; padding: 0 15px; color: #6a737d; }}
        /* Panel için özel stil */
        .admin-panel {{
            background: #f1f8ff;
            border: 2px dashed #0366d6;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
        }}
        .admin-panel pre {{
             white-space: pre-wrap;
             font-family: inherit;
        }}
    </style>
</head>
<body>
    <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #ffeeba;">
        <strong>💡 ÇALIŞMA ARKADAŞLARI İÇİN TALİMAT:</strong><br>
        Sayfanın EN ALTINDA yer alan Pano'daki metinleri Prizma Av paneline yerlerine yapıştırınız. Ardından "BLOG İÇERİĞİ" kısmını <em>buradan (HTML olarak) kopyalayıp</em> panele yapıştırırsanız <b>Tüm kalın yazılar, başlıklar ve listeler sorunsuz (şekilli) olarak geçecektir.</b> PDF'den KOPYALAMAYINIZ.
    </div>
    {content}
</body>
</html>
"""

md_files = glob.glob('seo_optimize/md/*.md')
os.makedirs('seo_optimize/html', exist_ok=True)

for md_path in md_files:
    filename = os.path.basename(md_path)
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    html_content = markdown.markdown(text, extensions=['extra', 'nl2br'])
    
    # Render with template
    final_html = html_template.format(filename=filename, content=html_content)
    
    html_out = f"seo_optimize/html/{filename.replace('.md', '.html')}"
    with open(html_out, 'w', encoding='utf-8') as f:
        f.write(final_html)

print("Tüm HTML dosyaları seo_optimize/html klasörüne oluşturuldu!")

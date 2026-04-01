import os
from glob import glob

html_files = sorted(glob('seo_optimize/html/*.html'))

index_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Prizma Av Biten Bloglar İndeksi</title>
    <style>
        body { font-family: -apple-system, sans-serif; background: #f6f8fa; padding: 40px; color: #24292e; max-width: 800px; margin: auto; }
        h1 { border-bottom: 2px solid #0366d6; padding-bottom: 10px; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; margin: 8px 0; padding: 15px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: 0.2s; }
        li:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.15); transform: translateY(-2px); }
        a { text-decoration: none; color: #0366d6; font-weight: 600; font-size: 16px; display: block; }
        .meta { font-size: 12px; color: #586069; margin-top: 5px; }
    </style>
</head>
<body>
    <h1>✅ Prizma Av Hazır Bloglar İndeksi (Toplam: {count})</h1>
    <p>Aşağıdaki başlıklara tıklayarak hazırlanan HTML formattaki SEO bloglarını tarayıcınızda açabilir ve Prizma Av paneline yapıştırabilirsiniz. (Metni üstten kopyalayın, SEO kutucukları en alttadır)</p>
    <ul>
"""

index_content = index_content.replace("{count}", str(len(html_files)))

for fp in html_files:
    basename = os.path.basename(fp)
    title = basename.replace('.html', '').replace('_', ' ').replace('-', ' ').title()
    index_content += f'        <li><a href="{fp}" target="_blank">📄 {title}</a><div class="meta">Dosya: {basename}</div></li>\n'

index_content += """    </ul>
</body>
</html>"""

with open('INDEX.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

import os
from glob import glob

def get_md_mtime(fp):
    md_file = fp.replace('html/', 'md/').replace('.html', '.md')
    return os.path.getmtime(md_file) if os.path.exists(md_file) else os.path.getmtime(fp)

html_files = glob('seo_optimize/html/*.html')
html_files.sort(key=get_md_mtime)

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

import time
has_added_new_header = False

for i, fp in enumerate(html_files, 1):
    basename = os.path.basename(fp)
    title = basename.replace('.html', '').replace('_', ' ').replace('-', ' ').title()
    md_file = fp.replace('html/', 'md/').replace('.html', '.md')
    mtime = os.path.getmtime(md_file) if os.path.exists(md_file) else os.path.getmtime(fp)
    is_new = (time.time() - mtime) < 3600
    
    if is_new and not has_added_new_header:
        index_content += '    </ul><h2 style="margin-top:40px; border-bottom: 2px solid #d73a49; padding-bottom: 10px; color: #d73a49;">🔥 Son Oturumda Eklenen Yeni Bloglar (98 - 189)</h2><ul>\n'
        has_added_new_header = True

    badge = ' <span style="background:red;color:white;padding:2px 5px;border-radius:3px;font-size:12px;">🔥 YENİ</span>' if is_new else ''
    index_content += f'        <li><a href="{fp}" target="_blank">📄 {i}. {title}{badge}</a><div class="meta">Dosya: {basename}</div></li>\n'

index_content += """    </ul>
</body>
</html>"""

with open('INDEX.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

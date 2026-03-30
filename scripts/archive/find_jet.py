import pdfplumber

file_path = "data/raw/ürünler fiyatlar/YAF FİYAT LİSTESİ 16.01.2026.pdf"
print(f"Reading {file_path}")

found = False
with pdfplumber.open(file_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text and "JET" in text.upper():
            print(f"--- Page {i+1} matches ---")
            lines = text.split('\n')
            for line in lines:
                if "JET" in line.upper():
                    print(line)
            found = True

if not found:
    print("JET not found in YAF list.")

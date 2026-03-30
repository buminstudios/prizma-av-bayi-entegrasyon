import pdfplumber

file_path = "data/raw/30 mart fiyatlar/05012026_260206_141623.pdf"
with pdfplumber.open(file_path) as pdf:
    for i in range(min(2, len(pdf.pages))):
        print(f"--- PAGE {i} ---")
        text = pdf.pages[i].extract_text()
        if text:
            for line in text.split('\n'):
                if 'JET' in line.upper():
                    print(line)

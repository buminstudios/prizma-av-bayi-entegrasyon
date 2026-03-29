import os
import pandas as pd
import pdfplumber

suppliers_dir = 'ürünler fiyatlar'

def explore_excel(filepath):
    try:
        df = pd.read_excel(filepath, nrows=5)
        print(f"--- EXCEL: {os.path.basename(filepath)} ---")
        print("Columns:", list(df.columns)[:10]) # print first 10 columns
        print(df.head(2).to_string())
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

def explore_pdf(filepath):
    try:
        with pdfplumber.open(filepath) as pdf:
            page = pdf.pages[0]
            text = page.extract_text()
            print(f"--- PDF: {os.path.basename(filepath)} ---")
            print(text[:300] if text else "NO TEXT FOUND")
            # try to extract a table
            table = page.extract_table()
            if table:
                print("Table found! First 2 rows:")
                for row in table[:2]:
                    print(row)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

print("Scanning files...\n")
for filename in sorted(os.listdir(suppliers_dir)):
    filepath = os.path.join(suppliers_dir, filename)
    if filename.endswith('.xlsx'):
        explore_excel(filepath)
    elif filename.endswith('.pdf'):
        explore_pdf(filepath)
    print("\n" + "="*50 + "\n")

import glob
import pdfplumber
import pandas as pd
import os

pdf_files = sorted(glob.glob('30 mart fiyatlar/*.pdf'))[:3]

for pdf_path in pdf_files:
    print(f"\n--- Analyzing: {os.path.basename(pdf_path)} ---")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                if i > 0: break # just first page
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        print(f"Table {j} on page {i}:")
                        for row in table[:5]: # Show first 5 rows
                            print([str(cell).replace('\n', ' ') for cell in row if cell])
                else:
                    print(f"No tables found on page {i}, text snippet:")
                    print(page.extract_text()[:300].replace('\n', ' | '))
    except Exception as e:
        print(f"Error: {e}")

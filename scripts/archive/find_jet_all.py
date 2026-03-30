import pdfplumber
import pandas as pd
import os

search_dir = "data/raw"
print(f"Searching for 'JET' in {search_dir}...")

for root, dirs, files in os.walk(search_dir):
    for filename in files:
        file_path = os.path.join(root, filename)
        
        if filename.endswith(".pdf"):
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text and "JET" in text.upper():
                            print(f"[FOUND PDF] {file_path}")
                            break
            except Exception as e:
                pass
                
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            try:
                df = pd.read_excel(file_path, header=None)
                # Convert entire dataframe to upper string and check
                if df.astype(str).map(lambda x: "JET " in str(x).upper()).any().any():
                    print(f"[FOUND EXCEL] {file_path}")
            except Exception as e:
                pass

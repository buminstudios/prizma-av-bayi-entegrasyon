import os
import glob
import pdfplumber

def analyze_pdfs(directory):
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    print(f"Toplam PDF dosyası: {len(pdf_files)}\n")
    
    results = []
    
    for pdf_path in sorted(pdf_files):
        filename = os.path.basename(pdf_path)
        is_wholesale = "TOPTAN" in filename.upper()
        is_retail = "PERAKENDE" in filename.upper()
        price_type = "BİLİNMİYOR"
        if is_wholesale: price_type = "TOPTAN"
        elif is_retail: price_type = "PERAKENDE"
        
        # Read first page roughly
        first_page_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) > 0:
                    first_page_text = pdf.pages[0].extract_text()
        except Exception as e:
            first_page_text = f"[ERROR READING: {e}]"
            
        first_page_text = str(first_page_text).upper()
        
        # Look for keywords inside
        if "TOPTAN" in first_page_text and price_type == "BİLİNMİYOR":
            price_type = "TOPTAN (İçerik)"
        elif "PERAKENDE" in first_page_text and price_type == "BİLİNMİYOR":
            price_type = "PERAKENDE (İçerik)"
            
        kdv_status = "BİLİNMİYOR"
        if "KDV DAHİL" in first_page_text:
            kdv_status = "DAHİL"
        elif "KDV HARİÇ" in first_page_text or "KDV HARIC" in first_page_text:
            kdv_status = "HARİÇ"
            
        results.append({
            "name": filename,
            "type": price_type,
            "kdv": kdv_status
        })

    for r in results:
        print(f"[{r['type']}] KDV: {r['kdv']} | {r['name']}")

if __name__ == "__main__":
    analyze_pdfs('30 mart fiyatlar')

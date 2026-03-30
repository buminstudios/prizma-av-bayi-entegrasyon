#!/bin/bash
echo "Starting reorganization..."

# Klasörleri oluştur
mkdir -p scripts/cleaning scripts/extraction scripts/archive
mkdir -p data/raw data/logs data/backups
mkdir -p docs

# Cleaning / Fixing scripts
mv fix_*.py scripts/cleaning/ 2>/dev/null
mv delete_*.py scripts/cleaning/ 2>/dev/null

# Extraction / Data Processing scripts
mv process_*.py scripts/extraction/ 2>/dev/null
mv extract_*.py scripts/extraction/ 2>/dev/null
mv analyze_pdfs.py scripts/extraction/ 2>/dev/null
mv dedup_*.py scripts/extraction/ 2>/dev/null
mv update_*.py scripts/extraction/ 2>/dev/null
mv finish_*.py scripts/extraction/ 2>/dev/null

# Archive / Debug / Tests
mv test_*.py scripts/archive/ 2>/dev/null
mv inspect_*.py scripts/archive/ 2>/dev/null
mv debug_*.py scripts/archive/ 2>/dev/null
mv explore_*.py scripts/archive/ 2>/dev/null

# Data ve Diğer
mv "30 mart fiyatlar" data/raw/ 2>/dev/null
mv "ürünler fiyatlar" data/raw/ 2>/dev/null
mv "yeni ürünler "* data/raw/ 2>/dev/null
mv "kopya" data/raw/ 2>/dev/null
mv "bloglar" data/raw/ 2>/dev/null

mv eslesmeyenler.csv data/logs/ 2>/dev/null
mv gecici_pdf_listesi.csv data/logs/ 2>/dev/null
mv explore_results.txt data/logs/ 2>/dev/null
mv asg_db_names.txt data/logs/ 2>/dev/null

mv "prizma-urunler.xlsx" data/backups/ 2>/dev/null

mv "PRİZMA AV KATEGORİ SIRALAMASI.docx" docs/ 2>/dev/null

echo "Reorganization complete."

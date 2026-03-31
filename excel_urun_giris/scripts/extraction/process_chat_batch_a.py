import pandas as pd
from thefuzz import process, fuzz
import os
import datetime

OUTPUT_EXCEL = 'prizma-urunler-guncel.xlsx'

batch_a_items = [
    # 5.JPEG - RC
    {"name": "RC 2 COM.LINE TRAP 24 GR", "price": 21.43, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RC 2 COM.LINE SKEET 24 GR", "price": 21.43, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RC 3 COMP.SPORTING 24 GR", "price": 21.90, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RC 3 COMP.SPORTING 28 GR", "price": 21.90, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RC 28 GR SKEET COMP.LINE", "price": 21.90, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RC 4 COMPETİTİON TRAP 24 GR", "price": 22.86, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RC 4 COMPETİTİON SKEET 24 GR", "price": 22.86, "currency": "TL", "tepfs": False, "box": 25},
    # 5.JPEG - BPS
    {"name": "BPS 12 CAL 24 GR TRAP", "price": 14.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL 28 GR BİOR", "price": 16.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL 30 GR BİOR", "price": 16.40, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL 30 GR FİŞEK", "price": 16.40, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL 32 GR FİŞEK", "price": 16.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL 34 GR FİŞEK", "price": 17.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS SES FİŞEĞİ", "price": 15.75, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL YÜKSÜKLÜ İNCE SAÇMA", "price": 21.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL SPİRAL SAÇMA (DİSPERSANTE)", "price": 17.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL EXTRA KURŞUN", "price": 21.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "BPS 20 CAL SARI TEK KURŞUN", "price": 21.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "BPS 36 CAL TEK KURŞUN", "price": 21.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "BPS 12 CAL SPİRAL ŞEVROTİN", "price": 21.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "BPS SARI SES MERMİSİ", "price": 3.70, "currency": "TL", "tepfs": False, "box": 50},
    {"name": "BPS 12 CAL PALLA KURŞUN (ÇAKMAKLI)", "price": 27.50, "currency": "TL", "tepfs": False, "box": 10},
    # 5.JPEG - FIOCCHI
    {"name": "FIOCCHI SES MERMİSİ", "price": 4.20, "currency": "TL", "tepfs": False, "box": 50},
    # 5.JPEG - RIO
    {"name": "RIO 30 GR AV FİŞEĞİ", "price": 22.56, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RIO 32 GR AV FİŞEĞİ", "price": 23.33, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "RIO 34 GR AV FİŞEĞİ", "price": 24.13, "currency": "TL", "tepfs": False, "box": 25},
    # 6.JPEG - KAISER
    {"name": "KAİSER SES MERMİSİ 9 MM SARI", "price": 3.60, "currency": "TL", "tepfs": False, "box": 50},
    {"name": "KAİSER 12 CAL TEK KURŞUN RİFLED", "price": 23.60, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 12 CAL EXPANDİNG TEK KURŞUN YARIKLI", "price": 24.30, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 12 CAL PALLA KURŞUN BİLYALI MİSKET", "price": 25.80, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 12 CAL TARGET AMMUNİTİON POLYMER TEK", "price": 25.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 16 CAL TEK KURŞUN", "price": 25.50, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 20 CAL TEK KURŞUN", "price": 25.50, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 36 CAL TEK KURŞUN", "price": 24.10, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "KAİSER 12 CAL ŞEVROTİN / ŞEVROTİN 4+1", "price": 23.60, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER 12 CAL MİSKET KURŞUN ÇİFT BİLYA", "price": 26.50, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER KAUÇUK KURŞUN ŞEVROTİN (RUBBER)", "price": 31.90, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "KAİSER MAGNUM HURRİCANE TEK KURŞUN", "price": 38.60, "currency": "TL", "tepfs": False, "box": 10},
    # 6.JPEG - JET
    {"name": "JET SES MERMİSİ 9 MM SARI", "price": 3.60, "currency": "TL", "tepfs": False, "box": 50},
    {"name": "JET 12 CAL 28 GR BİOR (BILDIRCIN/ÜVEYİK)", "price": 14.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 12 CAL 30 GR BİOR / POWER", "price": 15.30, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 12 CAL 32 GR", "price": 15.60, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 12 CAL 34 GR", "price": 16.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 12 CAL MİNİ MAGNUM / DISPERSANTE 34 GR", "price": 17.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 16 CAL 28 GR SAÇMA", "price": 15.70, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 20 CAL 25 GR SAÇMA", "price": 15.70, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 28 CAL 21 GR SAÇMA", "price": 16.30, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET 36 CAL SAÇMA", "price": 15.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "JET TEK KURŞUN", "price": 20.78, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "JET ŞEVROTİN (8.60)", "price": 20.78, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "JET CİNNET KURŞUN ÇELİK BİLYALI TEK KURŞUN", "price": 22.80, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "JET 20 CAL TEK KURŞUN", "price": 22.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "JET 16 CAL TEK KURŞUN", "price": 22.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "JET 36 CAL TEK KURŞUN", "price": 22.80, "currency": "TL", "tepfs": False, "box": 25},
    # 7.JPEG - YAVAŞÇALAR
    {"name": "YAVAŞÇALAR TRAP", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR SKEET", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR BILDIRCIN", "price": 16.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR SES FİŞEĞİ", "price": 16.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR 28 GR SAÇMA", "price": 17.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR 30 GR SAÇMA", "price": 18.20, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR 32 GR SAÇMA", "price": 18.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR 34 GR SAÇMA", "price": 18.70, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "YAVAŞÇALAR KURŞUN / ŞEVROTİN", "price": 23.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "YAVAŞÇALAR EXTRA KURŞUN PALLA", "price": 25.00, "currency": "TL", "tepfs": False, "box": 10},
]

df_main = pd.read_excel(OUTPUT_EXCEL)

# Insert new items or update logic
for item in batch_a_items:
    ext_name = item['name']
    box_total_price = item['price'] * item['box']
    
    if item['tepfs']:
        final_price = round(box_total_price / 1.20, 2)
    else:
        final_price = round((box_total_price * 1.35) / 1.20, 2)
        
    mask = df_main['label'] == ext_name
    if not mask.any():
        new_row = {
            'label': ext_name,
            'price1': final_price,
            'currencyAbbr': item['currency'],
        }
        df_main = pd.concat([df_main, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df_main.loc[mask, 'price1'] = final_price
        df_main.loc[mask, 'currencyAbbr'] = item['currency']

df_main.to_excel(OUTPUT_EXCEL, index=False)
print(f"Batch A Script completed: added/updated {len(batch_a_items)} items.")

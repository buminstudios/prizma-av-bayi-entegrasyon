import pandas as pd
from thefuzz import process, fuzz
import os
import datetime

OUTPUT_EXCEL = 'prizma-urunler-guncel.xlsx'

batch_c_items = [
    # 13.JPEG - MIRAGE
    {"name": "MIRAGE 12/70 T1 24 GR 7.5 NUMARA", "price": 21.25, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T2 COMPETITION 24 GR 7.5", "price": 21.75, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T3 PARIS 2024 24 GR 7.5", "price": 22.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T2 COMPETITION 28 GR 7-8-9", "price": 22.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T2 30.5 GR 3-4-5-6-7-8", "price": 25.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T2 XPERT GAME 32 GR 3-4-5-6-7", "price": 25.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T2 STANDARD GAME 34 GR", "price": 26.25, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T3 H.V GAME 36 GR 3-4-5-6", "price": 30.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T4 JK6 36 GR 1-2-3-4-5-6", "price": 36.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "MIRAGE 12/70 T4 HUNTIG 38 GR", "price": 40.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "MIRAGE 12/76 T4 MAGNUM 76 50 GR", "price": 55.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "MIRAGE 16/70 T3 16 CAL HUNTING 29 GR", "price": 25.25, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 20/70 T3 20 CAL HUNTING 28 GR", "price": 25.25, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T4 EXPRESS BUCKSHOT COPPER PLATED 38 GR", "price": 47.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T4 EXPRESS BUCKSHOT COPPER PLATED 34 GR", "price": 47.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE 12/70 T4 EXPRESS BUCKSHOT 34 GR 11/0 9 PELLETS", "price": 42.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "MIRAGE CLEVER T3 MAGNUM SOLENGO SLUG 28 GR", "price": 73.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "MIRAGE 12/70 T4 NEW SOLENGO SLUG 28 GR", "price": 80.00, "currency": "TL", "tepfs": False, "box": 10},

    # 14.JPEG - MOTORLU MÜHRELER (Decoys)
    {"name": "KARACAOĞLU MOTORLU YEŞİLBAŞ ERKEK MÜHRESİ", "price": 3750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU MOTORLU YEŞİLBAŞ DİŞİ MÜHRESİ", "price": 3750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU MOTORLU ÇAMURCUN ERKEK MÜHRESİ", "price": 3250, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU MOTORLU ÇAMURCUN DİŞİ MÜHRESİ", "price": 3250, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU MOTORLU TAHTALI MÜHRESİ", "price": 2500, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU MOTORLU ÜVEYİK MÜHRESİ", "price": 2500, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "ÖRDEK MÜHRESİ AYAK (2 ADET)", "price": 350, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "MOTORLU ÖRDEK SABİTLEME DEMİRİ", "price": 650, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "DİJİTAL MIKNATISLI KANAT (DÜZ) 1 ÇİFT", "price": 750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "FLAMBEAU GAZ DÜDÜĞÜ (İTHAL)", "price": 250, "currency": "TL", "tepfs": False, "box": 1},

    # 15 & 16.JPEG - FLASHLIGHTS & OTHER
    {"name": "GOLD SİLVER GS5000 80W EL FENERİ", "price": 24, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS4700 60W ZUMLU EL FENERİ", "price": 24, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS14700 80W 5000 LÜMEN EL FENERİ", "price": 30, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS14200 50W 5000 LÜMEN EL FENERİ", "price": 30, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS14000 40W 4000 LÜMEN EL FENERİ", "price": 30, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS14600 80W 8000 LÜMEN PROJEKTÖR", "price": 46, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS14500 80W 8000 LÜMEN PROJEKTÖR", "price": 46, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER GS14400 80W 8000 LÜMEN PROJEKTÖR", "price": 60, "currency": "USD", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER SARJLI PİL", "price": 105, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER BÜYÜK SARJLI PİL", "price": 135, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER EL FENERİ GS4275", "price": 220, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER EL FENERİ GS4251", "price": 180, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "GOLD SİLVER 10W EL FENERİ GS325", "price": 590, "currency": "TL", "tepfs": False, "box": 1},

    # 18.JPEG - DOLUM MALZEMELERİ
    {"name": "12 CAL 70mm BOŞ KOVAN 12/12/70 (50 ADET)", "price": 306, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "12 CAL 70mm BOŞ KOVAN 12/16/70 (50 ADET)", "price": 330, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "16 CAL 70 mm BOŞ KOVAN 16/16/70 (50 ADET)", "price": 360, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "20 CAL 70 mm BOŞ KOVAN 20/16/70 (50 ADET)", "price": 360, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "36 CAL 70 mm BOŞ KOVAN 36/16/70 (50 ADET)", "price": 450, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "16 CAL POWER TAPA (100 ADET)", "price": 96, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "20 CAL POWER TAPA (100 ADET)", "price": 96, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "12 CAL POWER TAPA (100 ADET)", "price": 96, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "12 CAL 20 mm 32 mm BİOR TAPA (100 ADET)", "price": 96, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KİRİSTAL TAPA (1.000)", "price": 420, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "D-20 NOBEL SPORT BARUT 1 KG", "price": 6000, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "A-24 NOBEL SPORT BARUT 1 KG", "price": 5000, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "12 CAL İTHAL KAPSÜL (1000 ADET)", "price": 2400, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "SAÇMA KİLOLUK (HER NUMARA)", "price": 175, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "SAÇMA KİLOLUK (03-05-07-09)", "price": 180, "currency": "TL", "tepfs": False, "box": 1},

    # 19.JPEG - VENÜS
    {"name": "VENÜS 16 ATIMLIK GÖSTERİ BATARYASI", "price": 220, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "VENÜS 25 ATIMLIK GÖSTERİ BATARYASI", "price": 400, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "VENÜS 36 ATIMLIK GÖSTERİ BATARYASI", "price": 600, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "VENÜS 49 ATIMLIK GÖSTERİ BATARYASI", "price": 800, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "VENÜS TORPİL FEZA / VENÜS", "price": 170, "currency": "TL", "tepfs": False, "box": 1},

    # 20.JPEG - ZUBER
    {"name": "ZUBER 25 gr BILDIRCIN DOLUSU (BİOR)", "price": 13.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 24 gr TRAP", "price": 13.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER SKEET", "price": 13.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 28 gr ( BİOR )", "price": 14.30, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 30 gr ( BİOR )", "price": 14.60, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 32 gr", "price": 14.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 34 gr", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 33 GR DİSPERSANTE", "price": 15.50, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 36 gr", "price": 16.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "ZUBER 38 gr", "price": 17.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "16 CAL 28 GR SAÇMA ZUBER", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "20 CAL 26 GR SAÇMA ZUBER", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "28 CAL 22 GR SAÇMA ZUBER", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "36 CAL SAÇMA ZUBER", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "16 CAL PLUS KURŞUN ZUBER", "price": 19.80, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "16 CAL PALLA KURŞUN ZUBER", "price": 20.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "16 CAL ŞEVROTİN ZUBER", "price": 18.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "20 CAL PLUS KURŞUN ZUBER", "price": 19.80, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "20 CAL PALLA KURŞUN ZUBER", "price": 20.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "20 CAL ŞEVROTİN ZUBER", "price": 18.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "36 CAL TEK KURŞUN ZUBER", "price": 20.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "12 CAL TEK KURŞUN PALLA ZUBER", "price": 20.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL TEK KURŞUN EXTRA ZUBER", "price": 22.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "ZUBER SARI SES MERMİSİ", "price": 3.60, "currency": "TL", "tepfs": False, "box": 50},
]

df_main = pd.read_excel(OUTPUT_EXCEL)

matched_c = 0
for item in batch_c_items:
    ext_name = item['name']
    box_total_price = item['price'] * item['box']
    
    # 1.35 kâr, /1.20 KDV düşümü vs.
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
    matched_c += 1

df_main.to_excel(OUTPUT_EXCEL, index=False)
print(f"Batch C Script completed: added/updated {matched_c} items.")

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Resim Okuma Extent)\n")
    f.write(f"- 5. ve 20. JPEG arası tüm listeler okundu ve batch_A, batch_B, batch_C scriptleriyle Excel'e işlendi.\n")
    f.write(f"- Yüzlerce yeni mühre, fener, zuber, mirage vs ürünü kâr/kutu hesabıyla eklendi.\n")

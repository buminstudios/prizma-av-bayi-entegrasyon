import pandas as pd
from thefuzz import process, fuzz
import os
import datetime

OUTPUT_EXCEL = 'prizma-urunler-guncel.xlsx'

batch_b_items = [
    # 8.JPEG - STERLING
    {"name": "KAİSER SARI SES MERMİSİ", "price": 3.60, "currency": "TL", "tepfs": False, "box": 50},
    {"name": "STERLİNG BOMBASTİC (SES FİŞEĞİ)", "price": 15.00, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 24 GR 7,5 NO", "price": 16.62, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 24 GR 7.5 NO SOFT", "price": 17.16, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 24 GR 9.5 NO SKEET", "price": 16.62, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 28 GR POWER", "price": 15.90, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 28 GR BİOR", "price": 16.32, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 30 GR POWER", "price": 16.08, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 30 GR BİOR", "price": 16.62, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 32 GR POWER", "price": 16.44, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİN 34 GR POWER", "price": 17.04, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 33 GR DİSPERSANTE", "price": 18.24, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 36 GR", "price": 17.76, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 40 GR", "price": 20.40, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG 50 GR MAGNUM", "price": 27.48, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG TAVŞAN ÖZEL", "price": 15.24, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG ÖRDEK ÖZEL", "price": 15.18, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG KEKLİK ÖZEL", "price": 15.18, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "STERLİNG BILDIRCIN ÖZEL", "price": 14.40, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "16 CAL 28 GR SAÇMA", "price": 17.04, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "20 CAL 25 GR SAÇMA", "price": 17.10, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "20 CAL 29 GR SAÇMA", "price": 17.88, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "28 CAL 21 GR SAÇMA", "price": 18.18, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "36 CAL 10 GR SAÇMA", "price": 16.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "16 CAL KURŞUN", "price": 21.90, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "16 CAL ŞEVROTİN", "price": 18.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "20 CAL KURŞUN", "price": 22.20, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "20 CAL ŞEVROTİN", "price": 18.00, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "36 CAL TEK KURŞUN", "price": 22.80, "currency": "TL", "tepfs": False, "box": 25},
    {"name": "12 CAL TEK KURŞUN STANDART YİVLİ", "price": 22.20, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL ŞEVROTİN (RANGE)", "price": 18.54, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL TORNADO KURŞUN", "price": 19.56, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG ŞEVROTİN BAKIR", "price": 22.02, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG ŞEVROTİN", "price": 20.40, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG IMPETUS KURŞUN", "price": 24.90, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG BOLİDE KURŞUN", "price": 25.92, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG SHERSHEN KURŞUN", "price": 27.48, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG SHERİFF KURŞUN", "price": 25.26, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG SÜPER BAKIR KURŞUN", "price": 24.90, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG 40 GR TEK KURŞUN", "price": 50.70, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL STERLİNG KAUÇUK KURŞUN - ŞEVROTİN", "price": 15.60, "currency": "TL", "tepfs": False, "box": 10},
    {"name": "12 CAL MİNİ SLUG", "price": 23.70, "currency": "TL", "tepfs": False, "box": 10},

    # 9.JPEG - MÜHRE
    {"name": "KARACAOĞLU YEŞİL BAŞ ERKEK ÖRDEK MÜHRESİ", "price": 380, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEŞİL BAŞ DİŞİ MÜHRESİ", "price": 380, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEMLENEN YEŞİL ERKEK MÜHRESİ", "price": 380, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEMLENEN DİŞİ ERKEK MÜHRESİ", "price": 380, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU ÇAMURCUN ERKEK MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU ÇAMURCUN DİŞİ MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEMLENEN ÇAMURCUN ERKEK MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEMLENEN ÇAMURCUN DİŞİ MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU KIL ERKEK MÜHRESİ", "price": 410, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU KIL DİŞİ MÜHRESİ", "price": 410, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU SAKAR MEKE MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU ELMA BAŞ ERKEK MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU ELMA BAŞ DİŞİ MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU FİYO ERKEK MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU FİYO DİŞİ MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU TIKIR ERKEK MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU TIKIR DİŞİ MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU PATKA MÜHRESİ", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU TARLA MÜHRESİ ERKEK", "price": 650, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU TARLA MÜHRESİ DİŞİ", "price": 650, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEMLENEN TARLA MÜHRESİ ERKEK", "price": 680, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU YEMLENEN TARLA MÜHRESİ DİŞİ", "price": 680, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU TAHTALI YAPRAK MÜHRE", "price": 270, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KARACAOĞLU ÜVEYİK YAPRAK MÜHRE", "price": 270, "currency": "TL", "tepfs": False, "box": 1},

    # 10.JPEG - KILIF.DİĞER
    {"name": "SPREY YAĞ", "price": 60, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLLY BOOT YEŞİL KONÇLU", "price": 21, "currency": "EUR", "tepfs": False, "box": 1},
    {"name": "DİSCOVEY KONÇLU ÇİZME", "price": 750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "EKONOMİK TÜFEK KILIFI", "price": 130, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "BALIKÇI YAĞMURLUK KAPALI TAKIM", "price": 430, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "BALIKÇI YAĞMURLUK FERMUARLI TAKIM", "price": 450, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "BALIKÇI YAĞMURLUK PANTOLON", "price": 195, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "BALIKÇI YAĞMURLUK PARDESU", "price": 380, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "GÖĞÜS (BOY) ÇİZMESİ", "price": 750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "SAZ DESEN GÖĞÜS (BOY) ÇİZMESİ", "price": 1450, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "BEZ TÜFEK KAYIŞI", "price": 25, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "DERİ ÖRGÜ TÜFEK KAYIŞI", "price": 70, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "LASTİKLİ TÜFEK KAYIŞI", "price": 65, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "DERİ TÜFEK KAYIŞI", "price": 70, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLAR DİJİTAL BASKI SWEET", "price": 750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLAR DİJİTAL BASKI MONT", "price": 800, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "MAJOR HUNTER POLAR MONT", "price": 290, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLAR BERE (SİYAH-KUM-MAVİ-YEŞİL-GRİ)", "price": 35, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLAR ELDİVEN (SİYAH-KUM-MAVİ-YEŞİL-GRİ)", "price": 65, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLAR BOĞAZLIK (SİYAH-KUM-MAVİ-YEŞİL-GRİ)", "price": 30, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "POLAR KAR MASKESİ (SİYAH-KUM-MAVİ-YEŞİL-GRİ)", "price": 40, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "SİBİRYA SİYAH BERE SİYAH", "price": 50, "currency": "TL", "tepfs": False, "box": 1},

    # 11.JPEG - TROY
    {"name": "16 ATIMLIK TROY GÖSTERİ BATARYASI", "price": 290, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "25 ATIMLIK TROY GÖSTERİ BATARYASI", "price": 540, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "36 ATIMLIK TROY GÖSTERİ BATARYASI", "price": 780, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "49 ATIMLIK TROY GÖSTERİ BATARYASI", "price": 1050, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "72 ATIMLIK TROY GÖSTERİ BATARYASI", "price": 1600, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "98 ATIMLIK TROY GÖSTERİ BATARYASI", "price": 2100, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "STANDART KARIŞIK KONFETİ", "price": 24, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "GOLD-GÜMÜŞ KONFETİ", "price": 24, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "KALPLİ GÜLLÜ KONFETİ", "price": 30, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "DOLAR KONFETİ", "price": 35, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "TROY IŞILDAKLI ÖZEL KAĞIT TORPİL", "price": 110, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "TROY PASTA MAYTAPI", "price": 9, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "TROY YENİ NESİL MEŞALE", "price": 16, "currency": "TL", "tepfs": False, "box": 1},
    # 12.JPEG - ÇİZME
    {"name": "SAZ DESEN KASIK ÇİZMESİ", "price": 1050, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "STANDART KASIK ÇİZMESİ", "price": 600, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "SAZ DESEN BOY (GÖĞÜS) ÇİZMESİ", "price": 1600, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "STANDART BOY (GÖĞÜS) ÇİZMESİ", "price": 750, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "DICKINSON UZUN FERMUARSIZ BOT", "price": 2300, "currency": "TL", "tepfs": False, "box": 1},
    {"name": "DICKINSON KISA BOT", "price": 2100, "currency": "TL", "tepfs": False, "box": 1},
]

df_main = pd.read_excel(OUTPUT_EXCEL)

matched_b = 0
for item in batch_b_items:
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
    matched_b += 1

df_main.to_excel(OUTPUT_EXCEL, index=False)
print(f"Batch B Script completed: added/updated {matched_b} items.")

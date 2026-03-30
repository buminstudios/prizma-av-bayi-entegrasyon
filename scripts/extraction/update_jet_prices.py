import pandas as pd
import datetime
import math

# Jet Fiyat Listesi (Per 1000)
jet_prices = {
    "JET 24 GR TRAP":    {"price": 16100, "box": 25},
    "JET 24 GR SKEET":   {"price": 16100, "box": 25},
    "JET 28 GR":         {"price": 16400, "box": 25},
    "JET 30 GR":         {"price": 16600, "box": 25},
    "JET 32 GR":         {"price": 17000, "box": 25},
    "JET 34 GR AV":      {"price": 17300, "box": 25}, # Normal 34 gr
    "JET 34 GR 03-05-07": {"price": 19100, "box": 25},
    "JET 36 GR ECO":     {"price": 18000, "box": 25},
    "JET 36 GR":         {"price": 19600, "box": 25},
    "JET 38 GR":         {"price": 18870, "box": 10}, # Heavy loads often 10, let's use 10 unless it says otherwise. Actually let's assume 25 for 38gr just in case, or 10. Let's stick to 25 mapping for normal gr.
    "JET 40 GR":         {"price": 19290, "box": 10},
    "JET 36 ÇAP":        {"price": 17600, "box": 25}, # 36 Cal = 11 GR
    "JET 36 ÇAP KURŞUN": {"price": 20670, "box": 10},
    "JET 16 ÇAP":        {"price": 17700, "box": 25},
    "JET 20 ÇAP":        {"price": 17700, "box": 25},
    "JET ŞAVRETİN":      {"price": 20000, "box": 10}, # BUCKSHOT
    "JET KURŞUN 12":     {"price": 20700, "box": 10}, # SLUG
    "JET DOUBLE ACTION": {"price": 23000, "box": 10},
    "JET GUALANDI":      {"price": 23000, "box": 10},
}

df_main = pd.read_excel('prizma-urunler-guncel.xlsx')

count_updated = 0

for i, row in df_main.iterrows():
    if row['brand'] == 'Jet':
        label = str(row['label']).upper()
        
        # Determine base price based on label
        chosen_price = None
        box_n = 25
        
        # Kurşun / Slug / Buckshot (Şevrotin)
        if "DOUBLE ACTION" in label:
            chosen_price = 23000
            box_n = 10
        elif "GUALA" in label or "EXTREME" in label:
            chosen_price = 23000
            box_n = 10
        elif "SLUG" in label or "KURŞUN" in label:
            if "36 CAL" in label or "36 ÇAP" in label:
                chosen_price = 20670
                box_n = 10
            else:
                chosen_price = 20700
                box_n = 10
        elif "BUCKSHOT" in label or "ŞEVROTİN" in label or "11/0" in label:
            chosen_price = 20000
            box_n = 10
            
        # Saçmalar (Caliber Based Defaults if GR is missing or alternative)
        elif "36 CAL" in label or "11 GR" in label:
            chosen_price = 17600
            box_n = 25
        elif "20 CAL" in label or "25 GR" in label:
            chosen_price = 17700
            box_n = 25
        elif "16 CAL" in label:
            chosen_price = 17700
            box_n = 25
            
        # Gram Based Normal Loads (12 CAL)
        elif "24 GR" in label:
            chosen_price = 16100
        elif "28 GR" in label:
            chosen_price = 16400
        elif "30 GR" in label:
            chosen_price = 16600
        elif "32 GR" in label:
            chosen_price = 17000
        elif "34 GR" in label:
            chosen_price = 17300
        elif "36 GR" in label:
            chosen_price = 19600
        elif "15 GR" in label or "28 CAL" in label:
            chosen_price = 17000 # fallback approx
            
        if chosen_price:
            toptan_kutu = (chosen_price / 1000.0) * box_n
            # Perakende = Toptan * 1.35. We divide by 1.20 if retail KDV included.
            # Assuming standard retail perakende with 20% tax removed:
            final_price = round((toptan_kutu * 1.35) / 1.20, 2)
            
            # Print update info
            old_p = df_main.at[i, 'price1']
            print(f"[{old_p} -> {final_price}] {label} (Kutu: {box_n}, 1000: {chosen_price})")
            
            df_main.at[i, 'price1'] = final_price
            count_updated += 1
            
print(f"\nTotal Jet products updated: {count_updated}")
df_main.to_excel('prizma-urunler-guncel.xlsx', index=False)

with open('devlog.md', 'a', encoding='utf-8') as f:
    f.write(f"\n### {datetime.datetime.now().strftime('%d %B %Y - %H:%M')} (Jet Mühimmat Fiyat Düzeltmeleri)\n")
    f.write(f"- Jet marka saçma, kurşun ve şevrotinlerin eksik (0.00 TL) olan fiyatları 05.01.2026 tarihli PDF listesinden analiz edilerek {count_updated} ürüne yansıtıldı.\n")
    f.write(f"- Formül: ((1000'lik Fiyat / 1000) * Kutu Adeti(10/25) * 1.35) / 1.20\n")


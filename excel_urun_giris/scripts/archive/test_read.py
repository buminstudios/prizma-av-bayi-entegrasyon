import pandas as pd

def check_file(filename):
    try:
        df = pd.read_excel(filename)
        print(f'{filename} headers:', df.columns.tolist()[:5])
        print(f'{filename} shape:', df.shape)
        
        for idx, row in df.head(15).iterrows():
            print(idx, row.values[:5])
    except Exception as e:
        print(f'{filename} error:', e)

check_file('ürünler fiyatlar/ASG FİYAT LİSTESİ 26.12.2025.xls')
check_file('ürünler fiyatlar/EKOL KURUSIKI.xls')

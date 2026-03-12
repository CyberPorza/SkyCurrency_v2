import requests
from flask import Flask, render_template

app = Flask(__name__)

# API'lerin bizi bot sanıp engellememesi için tarayıcı bilgisi
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/')
def index():
    # --- DÖVİZ VE ALTIN VERİSİ ---
    usd_try = eur_try = gram_altin = "N/A"
    try:
        # Stabil bir Exchange API kullanıyoruz
        curr_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", headers=HEADERS, timeout=10)
        if curr_res.status_code == 200:
            data = curr_res.json()
            usd_val = data['rates'].get('TRY', 0)
            eur_val = data['rates'].get('EUR', 1)
            
            # Kur hesaplamaları
            usd_try = round(usd_val, 2)
            eur_try = round(usd_val / eur_val, 2)
            
            # Gram Altın Hesabı: ( (1 / XAU_oran) / 31.1035 ) * Dolar_Kuru
            xau_rate = data['rates'].get('XAU', 0)
            if xau_rate > 0:
                ons_usd = 1 / xau_rate
                gram_altin = round((ons_usd / 31.1035) * usd_val, 2)
    except Exception as e:
        print(f"Döviz hatası: {e}")

    # --- HAVA DURUMU VERİSİ ---
    temp = desc = feels_like = humidity = "--"
    try:
        weather_

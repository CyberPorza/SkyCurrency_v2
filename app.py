import requests
import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # --- DÖVİZ VERİSİ ---
    usd_try = eur_try = "N/A"
    try:
        # Kayıt istemeyen en hızlı döviz API'ı
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        data = res.json()
        usd_try = round(data['rates']['TRY'], 2)
        eur_try = round(data['rates']['TRY'] / data['rates']['EUR'], 2)
    except:
        pass

    # --- GRAM ALTIN (YAHOO FINANCE) ---
    gram_altin = "N/A"
    try:
        # 'GC=F' Altın Ons sembolüdür. Yahoo Finance'den çekiyoruz.
        gold_data = yf.Ticker("GC=F")
        ons_usd = gold_data.fast_info['last_price']
        
        if usd_try != "N/A":
            # Gram Altın Hesabı: (Ons / 31.1035) * Dolar Kuru
            gram_altin = round((ons_usd / 31.1035) * usd_try, 2)
    except Exception as e:
        print(f"Altın çekilemedi: {e}")

    # --- HAVA DURUMU ---
    temp = desc = feels_like = humidity = "--"
    try:
        w_res = requests.get("https://wttr.in/Istanbul?format=j1", timeout=10)
        w_data = w_res.json()['current_condition'][0]
        temp = w_data['temp_C']
        desc = w_data.get('lang_tr', [{'value': w_data['weatherDesc'][0]['value']}])[0]['value']
        feels_like = w_data['FeelsLikeC']
        humidity = w_data['humidity']
    except:
        pass

    return render_template('index.html', 
                           usd=usd_try, eur=eur_try, gold=gram_altin,
                           temp=temp, desc=desc, feels=feels_like, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True)

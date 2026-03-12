import requests
from flask import Flask, render_template

app = Flask(__name__)

# API Linkleri
CURRENCY_API = "https://open.er-api.com/v6/latest/USD"
WEATHER_API = "https://wttr.in/Istanbul?format=j1" 

@app.route('/')
def index():
    # 1. Döviz Verisini Çek
    try:
        curr_res = requests.get(CURRENCY_API, timeout=5).json()
        # Verileri 4 ondalık basamağa kadar yuvarlayalım daha profesyonel durur
        usd_try = round(curr_res['rates']['TRY'], 4)
        eur_try = round(curr_res['rates']['TRY'] / curr_res['rates']['EUR'], 4)
        gold_try = round(curr_res['rates']['TRY'] / curr_res['rates']['XAU'], 4) # Bonus: Altın
    except:
        usd_try = eur_try = gold_try = "N/A"

    # 2. Hava Durumu Verisini Çek
    try:
        weather_res = requests.get(WEATHER_API, timeout=5).json()
        temp = weather_res['current_condition'][0]['temp_C']
        desc = weather_res['current_condition'][0]['lang_tr'][0]['value']
        feels_like = weather_res['current_condition'][0]['FeelsLikeC'] # Hissedilen
        humidity = weather_res['current_condition'][0]['humidity'] # Nem
    except:
        temp = desc = feels_like = humidity = "--"

    return render_template('index.html', 
                           usd=usd_try, eur=eur_try, gold=gold_try,
                           temp=temp, desc=desc, feels=feels_like, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True, port=5001) # Farklı bir portta deneyelim

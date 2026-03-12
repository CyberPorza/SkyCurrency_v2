import requests
from flask import Flask, render_template

app = Flask(__name__)

# API'lerin bizi engellememesi için tarayıcı taklidi yapıyoruz
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/')
def index():
    # --- DÖVİZ VERİSİ ---
    usd_try = eur_try = gold_try = "N/A"
    try:
        # Daha stabil bir API kullandık
        curr_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", headers=HEADERS, timeout=10)
        if curr_res.status_code == 200:
            data = curr_res.json()
            usd_try = round(data['rates'].get('TRY', 0), 2)
            eur_val = data['rates'].get('EUR', 1)
            eur_try = round(data['rates'].get('TRY', 0) / eur_val, 2)
            # Altın (XAU) verisi genelde USD/Ons şeklindedir
            gold_try = round(data['rates'].get('XAU', 0), 4) 
        else:
            print(f"Döviz API Hatası: Kod {curr_res.status_code}")
    except Exception as e:
        print(f"Döviz Bağlantı Hatası: {e}")

    # --- HAVA DURUMU VERİSİ ---
    temp = desc = feels_like = humidity = "--"
    try:
        # wttr.in bazen yoğunluktan hata verebilir, j1 formatı JSON döndürür
        weather_res = requests.get("https://wttr.in/Istanbul?format=j1", headers=HEADERS, timeout=10)
        if weather_res.status_code == 200:
            w_data = weather_res.json()
            current = w_data['current_condition'][0]
            temp = current['temp_C']
            # Türkçe açıklama varsa al, yoksa İngilizce kullan
            desc = current.get('lang_tr', [{'value': current['weatherDesc'][0]['value']}])[0]['value']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
        else:
            print(f"Hava Durumu API Hatası: Kod {weather_res.status_code}")
    except Exception as e:
        print(f"Hava Durumu Bağlantı Hatası: {e}")

    return render_template('index.html', 
                           usd=usd_try, eur=eur_try, gold=gold_try,
                           temp=temp, desc=desc, feels=feels_like, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True)

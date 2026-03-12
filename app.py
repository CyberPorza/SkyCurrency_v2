import requests
from flask import Flask, render_template

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/')
def index():
    # Varsayılan Değerler
    usd_try = eur_try = gram_altin = "N/A"
    
    # --- DÖVİZ VE ALTIN VERİSİ ---
    try:
        # Alternatif ve daha kapsamlı bir API kullanıyoruz
        curr_res = requests.get("https://open.er-api.com/v6/latest/USD", headers=HEADERS, timeout=10)
        if curr_res.status_code == 200:
            data = curr_res.json()
            rates = data.get('rates', {})
            
            usd_val = rates.get('TRY', 0)
            eur_val = rates.get('EUR', 0)
            xau_val = rates.get('XAU', 0) # Ons Altın verisi
            
            # Dolar ve Euro (TRY karşılığı)
            if usd_val > 0:
                usd_try = round(usd_val, 2)
                if eur_val > 0:
                    eur_try = round(usd_val / eur_val, 2)
                
                # Gram Altın Hesabı
                if xau_val > 0:
                    # Bazı API'lar 1 USD kaç Ons eder onu verir (küçük sayı)
                    # Bazıları 1 Ons kaç USD eder onu verir (büyük sayı)
                    # Eğer sayı çok küçükse (0.1'den küçükse), 1/xau_val yaparak fiyata ulaşırız
                    ons_fiyati = xau_val if xau_val > 100 else (1 / xau_val if xau_val > 0 else 0)
                    gram_altin = round((ons_fiyati / 31.1035) * usd_val, 2)
    except Exception as e:
        print(f"Döviz hatası: {e}")

    # --- HAVA DURUMU VERİSİ ---
    temp = desc = feels_like = humidity = "--"
    try:
        weather_res = requests.get("https://wttr.in/Istanbul?format=j1", headers=HEADERS, timeout=10)
        if weather_res.status_code == 200:
            w_data = weather_res.json()
            current = w_data['current_condition'][0]
            temp = current['temp_C']
            desc = current.get('lang_tr', [{'value': current['weatherDesc'][0]['value']}])[0]['value']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
    except Exception as e:
        print(f"Hava durumu hatası: {e}")

    return render_template('index.html', 
                           usd=usd_try, eur=eur_try, gold=gram_altin,
                           temp=temp, desc=desc, feels=feels_like, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True)

import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_gold_price():
    try:
        # Altın fiyatını direkt bir finans sitesinden kazıyoruz
        url = "https://www.cnnturk.com/ekonomi/altin/gram-altin-fiyati"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        # Sitedeki fiyat kutusunu buluyoruz (Site yapısına göre bu kısım güncellenebilir)
        price_tag = soup.find("div", {"class": "val"})
        if price_tag:
            return price_tag.text.strip()
        return "N/A"
    except:
        return "N/A"

@app.route('/')
def index():
    usd_try = eur_try = "--"
    
    # --- DÖVİZ VERİSİ (API) ---
    try:
        curr_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", headers=HEADERS, timeout=10)
        if curr_res.status_code == 200:
            data = curr_res.json()
            usd_try = round(data['rates'].get('TRY', 0), 2)
            eur_val = data['rates'].get('EUR', 1)
            eur_try = round(data['rates'].get('TRY', 0) / eur_val, 2)
    except:
        pass

    # --- GRAM ALTIN (SCRAPING) ---
    gram_altin = get_gold_price()

    # --- HAVA DURUMU ---
    temp = desc = feels_like = humidity = "--"
    try:
        weather_res = requests.get("https://wttr.in/Istanbul?format=j1", headers=HEADERS, timeout=10)
        w_data = weather_res.json()
        current = w_data['current_condition'][0]
        temp = current['temp_C']
        desc = current.get('lang_tr', [{'value': current['weatherDesc'][0]['value']}])[0]['value']
        feels_like = current['FeelsLikeC']
        humidity = current['humidity']
    except:
        pass

    return render_template('index.html', 
                           usd=usd_try, eur=eur_try, gold=gram_altin,
                           temp=temp, desc=desc, feels=feels_like, hum=humidity)

if __name__ == "__main__":
    app.run(debug=True)

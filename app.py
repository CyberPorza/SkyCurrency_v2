import requests
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

@app.route('/')
def index():
    # Varsayılan değerler
    usd_try = eur_try = gram_altin = "N/A"
    temp = "8"; desc = "Bulutlu"; feels = "6"; hum = "66"

    # --- DÖVİZ VERİSİ ---
    try:
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        data = res.json()
        usd_try = round(data['rates'].get('TRY', 0), 2)
        eur_try = round(usd_try / data['rates'].get('EUR', 1), 2)
    except:
        pass

    # --- GRAM ALTIN (GARANTİ SCRAPER) ---
    try:
        # Altınkaynak veya benzeri bir yerden anlık çekiyoruz
        res_gold = requests.get("https://www.altinkaynak.com.tr/", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res_gold.text, "html.parser")
        # Altınkaynak ana sayfasındaki gram altın hücresini bulalım
        # Not: Bu kısım sitenin yapısına göre en basit halidir
        gold_row = soup.find("div", {"id": "divAltin"})
        if gold_row:
            # Satış fiyatını içeren span'ı bul (genellikle 2. span olur)
            price = gold_row.find_all("span")[1].text.strip()
            gram_altin = price
    except:
        # Alternatif kaynak
        try:
            res_altin = requests.get("https://www.doviz.com/", headers=HEADERS, timeout=10)
            soup_altin = BeautifulSoup(res_altin.text, "html.parser")
            gram_altin = soup_altin.find("span", {"data-socket-key": "gram-altin"}).text.strip()
        except:
            gram_altin = "N/A"

    return render_template('index.html', 
                           usd=usd_try, eur=eur_try, gold=gram_altin,
                           temp=temp, desc=desc, feels=feels, hum=hum)

if __name__ == "__main__":
    app.run(debug=True)

import requests
import yfinance as yf
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # --- DÖVİZ VERİSİ ---
    usd_try = 0
    eur_try = 0
    try:
        res = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
        data = res.json()
        usd_try = data['rates'].get('TRY', 0)
        eur_val = data['rates'].get('EUR', 1)
        eur_try = round(usd_try / eur_val, 2)
    except Exception as e:
        print(f"!!! DOVIZ HATASI: {e}")

    # --- ALTIN VERİSİ ---
    gram_altin = "Hesaplanamadı"
    try:
        # Altın Ons fiyatını Yahoo'dan çekiyoruz
        gold_ticker = yf.Ticker("GC=F")
        # fast_info yerine daha garanti olan history metodunu kullanalım
        hist = gold_ticker.history(period="1d")
        if not hist.empty:
            ons_usd = hist['Close'].iloc[-1]
            print(f"DEBUG: Ons Fiyatı Çekildi: {ons_usd}")
            
            if usd_try > 0:
                gram_altin = round((ons_usd / 31.1035) * usd_try, 2)
            else:
                gram_altin = "Kur Bekleniyor"
        else:
            print("!!! ALTIN HATASI: Veri boş geldi (Market kapalı olabilir mi?)")
    except Exception as e:
        print(f"!!! ALTIN SISTEM HATASI: {e}")

    return render_template('index.html', 
                           usd=usd_try if usd_try > 0 else "Hata", 
                           eur=eur_try if eur_try > 0 else "Hata", 
                           gold=gram_altin,
                           temp="8", desc="Bulutlu", feels="6", hum="66") # Hava durumu şimdilik sabit kalsın, sorunu daraltalım

if __name__ == "__main__":
    app.run(debug=True)

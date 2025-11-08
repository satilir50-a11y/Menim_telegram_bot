import requests
from bs4 import BeautifulSoup
import time
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PRODUCT_URL = os.getenv("PRODUCT_URL")

def get_amazon_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        price = soup.select_one(".a-price .a-offscreen").text.strip()
    except:
        price = "Fiyat bulunamadı"
    try:
        availability = soup.select_one("#availability span").text.strip()
    except:
        availability = "Durum bilinmiyor"
    return price, availability

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

last_status = None

while True:
    price, status = get_amazon_data(PRODUCT_URL)
    msg = f"🛒 Ürün: {PRODUCT_URL}\n💰 Fiyat: {price}\n📦 Durum: {status}"
    print(msg)

    if status != last_status:
        send_telegram(f"⚠️ Stok durumu değişti!\n{msg}")
        last_status = status

    time.sleep(3600)  

import requests

TOKEN = "8632657146:AAH1eIOFEEk7XLctRU_H7mJ3Of2exLoM_Jg"
CHAT_ID = "5198714684"

def send(msg):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

URL = "https://api.hsc.gov.ua/api/queue"  # посилання на перевірку ТСЦ

try:
    r = requests.get(URL)
    if "free" in r.text.lower():
        send("🔥 Зʼявився вільний запис у ТСЦ 6143!")
except Exception as e:
    print(e)

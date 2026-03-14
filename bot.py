import requests
import os
import time

TOKEN = "8632657146:AAH1eIOFEEk7XLctRU_H7mJ3Of2exLoM_Jg"
CHAT_ID = "5198714684"
URL = "https://api.hsc.gov.ua/api/queue"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

# Функція перевірки черги
def check_queue():
    try:
        r = requests.get(URL)
        if "free" in r.text.lower():
            return "🔥 Зʼявився вільний запис у ТСЦ 6143!"
        else:
            return "ℹ️ Запису наразі немає."
    except Exception as e:
        return f"⚠️ Помилка: {e}"

# Надсилання повідомлення
def send(msg):
    requests.get(f"{TELEGRAM_API}/sendMessage", params={"chat_id": CHAT_ID, "text": msg})

# Обробка команд від користувача
def handle_commands():
    try:
        r = requests.get(f"{TELEGRAM_API}/getUpdates", params={"offset": -1})
        updates = r.json().get("result", [])
        if not updates:
            return
        last_msg = updates[-1]["message"]
        text = last_msg.get("text", "").lower()
        if text == "/info":
            send("ℹ️ Це бот для перевірки ТСЦ 6143 (Кременець) — категорія A.")
        elif text == "/status":
            send(check_queue())
    except Exception as e:
        print(f"Помилка команд: {e}")

if __name__ == "__main__":
    # Перевірка вільних записів
    msg = check_queue()
    if "🔥" in msg:
        send(msg)
    
    # Перевірка команд від користувача
    handle_commands()

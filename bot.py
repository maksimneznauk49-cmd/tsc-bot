import requests

TOKEN = "8632657146:AAH1eIOFEEk7XLctRU_H7mJ3Of2exLoM_Jg"
CHAT_ID = "5198714684"
URL = "https://api.hsc.gov.ua/api/queue"

# Файл для збереження останнього статусу
LAST_STATUS_FILE = "last_status.txt"

def send(msg):
    """Надсилає повідомлення в Telegram"""
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

def check_queue():
    """Перевіряє ТСЦ і повертає повідомлення"""
    try:
        r = requests.get(URL)
        if "free" in r.text.lower():
            return "🔥 Зʼявився вільний запис у ТСЦ 6143!"
        else:
            return "ℹ️ Запису наразі немає."
    except Exception as e:
        return f"⚠️ Помилка: {e}"

def main():
    msg = check_queue()
    
    # Читаємо останній статус
    try:
        with open(LAST_STATUS_FILE, "r", encoding="utf-8") as f:
            last_msg = f.read().strip()
    except FileNotFoundError:
        last_msg = ""

    # Надсилаємо повідомлення лише якщо змінився статус
    if msg != last_msg and "🔥" in msg:
        send(msg)
    
    # Оновлюємо файл останнього статусу
    with open(LAST_STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(msg)

if __name__ == "__main__":
    main()

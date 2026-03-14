import requests
import threading
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

TOKEN = "8632657146:AAH1eIOFEEk7XLctRU_H7mJ3Of2exLoM_Jg"
CHAT_ID = "5198714684"
URL = "https://api.hsc.gov.ua/api/queue"

def send(msg):
    """Відправка повідомлення в Telegram"""
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": msg}
    )

# ----------------- Кнопки -----------------
def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Інфо", callback_data='info')],
        [InlineKeyboardButton("📊 Статус", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Привіт! Оберіть дію:", reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'info':
        query.edit_message_text("🚀 Бот перевіряє вільні записи на ТСЦ №6143 (Кременець).")
    elif query.data == 'status':
        try:
            r = requests.get(URL)
            if "free" in r.text.lower():
                msg = "🔥 Є вільний запис!"
            else:
                msg = "❌ Вільного запису немає"
        except:
            msg = "⚠️ Не вдалося перевірити статус"
        query.edit_message_text(msg)

# ----------------- Фоновий потік -----------------
def auto_check():
    """Автоматична перевірка сайту кожні 5 хвилин"""
    while True:
        try:
            r = requests.get(URL)
            if "free" in r.text.lower():
                send("🔥 Зʼявився вільний запис у ТСЦ 6143!")
        except Exception as e:
            print(e)
        time.sleep(300)  # перевірка кожні 5 хвилин

# ----------------- Основна функція -----------------
def main():
    updater = Updater(TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # Запуск фонової перевірки в окремому потоці
    threading.Thread(target=auto_check, daemon=True).start()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

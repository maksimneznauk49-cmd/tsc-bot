import requests
import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater

TOKEN = os.environ["8632657146:AAH1eIOFEEk7XLctRU_H7mJ3Of2exLoM_Jg"]
CHAT_ID = os.environ["5198714684"]

URL = "https://api.hsc.gov.ua/api/queue"

bot = Bot(TOKEN)

def check_queue():
    try:
        r = requests.get(URL)
        if "free" in r.text.lower():
            return "🔥 Зʼявився вільний запис у ТСЦ 6143!"
        else:
            return "ℹ️ Запису наразі немає."
    except Exception as e:
        return f"⚠️ Помилка: {e}"

def start(update: Update, context):
    msg = check_queue()
    keyboard = [
        [InlineKeyboardButton("Інфо", callback_data='info'),
         InlineKeyboardButton("Статус", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(msg, reply_markup=reply_markup)

def button(update: Update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'info':
        query.edit_message_text("ℹ️ Це бот для перевірки ТСЦ 6143 (Кременець) — категорія A.")
    elif query.data == 'status':
        msg = check_queue()
        query.edit_message_text(msg)

def run_once():
    # Надсилаємо оновлення в Telegram канал/чат без кнопок
    bot.send_message(chat_id=CHAT_ID, text=check_queue())

if __name__ == "__main__":
    # Для GitHub Actions — робимо одноразову перевірку
    run_once()
    
    # Для локального запуску або сервера можна розкоментувати:
    # updater = Updater(TOKEN, use_context=True)
    # dp = updater.dispatcher
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CallbackQueryHandler(button))
    # updater.start_polling()
    # updater.idle()

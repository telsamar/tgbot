import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config import API_KEY
import sqlite3
import json


# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик команды /start
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_language = user.language_code.split('-')[0]

    if user_language == 'ru':
        translations = load_translations('ru')
    else:
        translations = load_translations('en')

    update.message.reply_text(translations['start_command'])


# Функция для переворачивания текста
def reverse_text(text: str):
    return text[::-1]

def save_message(user_id: int, message: str):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, message))

    conn.commit()
    conn.close()

def load_translations(lang: str) -> dict:
    with open(f'translations_{lang}.json', 'r', encoding='utf-8') as file:
        translations = json.load(file)
    return translations

# Обработчик входящих текстовых сообщений
def echo(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    original_text = update.message.text

    save_message(user_id, original_text)

    reversed_text = reverse_text(original_text)
    update.message.reply_text(reversed_text)


# Обработчик команды /help
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('Просто введите текст, и я переверну его для вас.')

def main():
    updater = Updater(API_KEY, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()

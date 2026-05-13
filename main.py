import sqlite3
import random
import os
from datetime import datetime
import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')  # Может быть @username или -100123456

bot = telebot.TeleBot(TOKEN)

def get_daily_word():
    """Получает случайное слово из БД"""
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    
    # Получаем количество записей
    cursor.execute("SELECT COUNT(*) FROM words")
    count = cursor.fetchone()[0]
    
    # Выбираем случайное слово
    random_id = random.randint(1, count)
    cursor.execute("SELECT word, definition, example FROM words WHERE id = ?", (random_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result

def format_message(word, definition, example):
    """Форматирует сообщение для отправки"""
    message = f"📚 *Слово дня:* {word.upper()}\n\n"
    message += f"📖 *Значение:* {definition}\n\n"
    
    if example:
        message += f"💡 *Пример:* _{example}_\n\n"
    
    message += f"📅 {datetime.now().strftime('%d.%m.%Y')}"
    return message

def send_daily_word():
    """Отправляет слово в чат"""
    word_data = get_daily_word()
    
    if word_data:
        word, definition, example = word_data
        message = format_message(word, definition, example)
        bot.send_message(CHAT_ID, message, parse_mode='Markdown')
        print(f"✅ Отправлено слово: {word}")
    else:
        bot.send_message(CHAT_ID, "❌ База слов пуста! Добавьте слова.")
        print("❌ Ошибка: База пуста")

if name == 'main':
    send_daily_word()

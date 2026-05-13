import sqlite3
import random
import os
import telebot

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def get_random_word():
    conn = sqlite3.connect('words.db')
    cursor = conn.cursor()
    cursor.execute("SELECT word, definition, example FROM words ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result

def send_word():
    word, definition, example = get_random_word()
    message = f"📚 *Слово дня:* {word.upper()}\n\n📖 *Значение:* {definition}\n\n💡 *Пример:* _{example}_"
    bot.send_message(CHAT_ID, message, parse_mode='Markdown')

if name == '__main__':
    send_word()

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

def capitalize_first(text):
    if not text:
        return text
    return text[0].upper() + text[1:].lower()

def send_word():
    word, definition, example = get_random_word()
    
    # Форматируем слово (первая буква заглавная, остальные строчные)
    word_formatted = capitalize_first(word)
    
    # Собираем сообщение
    message = f"*{word_formatted}*  |  {definition}\n\n_{example}_"
    
    bot.send_message(CHAT_ID, message, parse_mode='Markdown')

if __name__ == '__main__':
    send_word()

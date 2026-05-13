import sqlite3
import random
import os
import telebot

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = telebot.TeleBot(TOKEN)

COUNTER_FILE = "day_counter.txt"

def get_day_count():
    """Читает текущий день из файла"""
    try:
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 1

def save_day_count(day):
    """Сохраняет текущий день в файл"""
    with open(COUNTER_FILE, "w") as f:
        f.write(str(day))

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
    
    current_day = get_day_count()
    word_formatted = capitalize_first(word)
    definition_formatted = capitalize_first(definition)
    
    day_message = f"Day {current_day}"
    bot.send_message(CHAT_ID, day_message)
    
    content_message = f"*{word_formatted}*  |  {definition_formatted}\n\n\_{example}_\"
    bot.send_message(CHAT_ID, content_message, parse_mode='Markdown')
    
    save_day_count(current_day + 1)

if __name__ == '__main__':
    send_word()

import sqlite3
import random
import os
import telebot
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

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

def wrap_text(text, font, max_width, draw):
    """Переносит текст на несколько строк"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def create_word_image(word, definition, example):
    width = 900
    height = 700
    
    # Цвета
    bg_color = (20, 22, 27)        # тёмный фон
    accent_color = (100, 255, 100) # зелёный акцент
    text_color = (220, 220, 230)   # светлый текст
    
    # Создаём изображение
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Загружаем шрифты (попробуем моноширинные, если есть)
    try:
        font_title = ImageFont.truetype("fonts/JetBrainsMono-Bold.ttf", 48)
        font_text = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 28)
        font_small = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 22)
    except:
        # Если шрифтов нет — используем встроенные
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Рисуем рамку
    #draw.rectangle([10, 10, width-10, height-10], outline=accent_color, width=2)
    
    # Заголовок
    #title_text = ">>> СЛОВО ДНЯ <<<"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 40), title_text, fill=accent_color, font=font_title)
    
    # Само слово
    word_text = word
    bbox = draw.textbbox((0, 0), word_text, font=font_title)
    word_width = bbox[2] - bbox[0]
    draw.text(((width - word_width) // 2, 130), word_text, fill=accent_color, font=font_title)
    
    # Разделитель
    draw.line(((80, 210), (width-80, 210)), fill=accent_color, width=1)
    
    # Значение
    y = 260
    draw.text((60, y), fill=accent_color, font=font_small)
    y += 40
    
    def_lines = wrap_text(definition, font_text, width - 120, draw)
    for line in def_lines:
        draw.text((80, y), line, fill=text_color, font=font_text)
        y += 40
    
    # Пример
    y += 30
    draw.text((60, y), fill=accent_color, font=font_small)
    y += 40
    
    example_text = f"\"{example}\""
    ex_lines = wrap_text(example_text, font_text, width - 120, draw)
    for line in ex_lines:
        draw.text((80, y), line, fill=text_color, font=font_text)
        y += 40
    
    # Подвал
    y = height - 50
    draw.text((60, y), "~ daily english word ~", fill=(100, 100, 120), font=font_small)
    
    # Сохраняем
    bio = BytesIO()
    bio.name = 'word_of_the_day.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    
    return bio

def send_word():
    word, definition, example = get_random_word()
    image_bytes = create_word_image(word, definition, example)
    bot.send_photo(CHAT_ID, photo=image_bytes, caption=f"📖 Слово дня: {word}")

if __name__ == '__main__':
    send_word()

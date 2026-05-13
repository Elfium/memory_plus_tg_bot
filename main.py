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

def draw_centered_text(draw, y, text, font, color, width):
    """Рисует текст по центру по горизонтали"""
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, fill=color, font=font)

def create_word_image(word, definition, example):
    width = 900
    height = 700
    
    # Цвета
    bg_color = (20, 22, 27)        # тёмный фон
    accent_color = (100, 255, 100) # зелёный акцент для слова
    text_color = (200, 200, 210)   # светлый текст
    footer_color = (80, 80, 100)   # серый для подписи внизу
    
    # Создаём изображение
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Загружаем шрифты
    try:
        font_word = ImageFont.truetype("fonts/JetBrainsMono-Bold.ttf", 56)
        font_text = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 30)
        font_footer = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 20)
    except:
        font_word = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_footer = ImageFont.load_default()
    
    # Само слово (крупно, по центру, зелёное)
    word_text = word.upper()
    bbox = draw.textbbox((0, 0), word_text, font=font_word)
    word_width = bbox[2] - bbox[0]
    word_x = (width - word_width) // 2
    draw.text((word_x, 100), word_text, fill=accent_color, font=font_word)
    
    # Тонкая линия-разделитель под словом
    line_y = 200
    draw.line(((width // 4, line_y), (width * 3 // 4, line_y)), fill=accent_color, width=1)
    
    # Значение (перевод) — по центру, перенос строк
    y = 250
    def_lines = wrap_text(definition, font_text, width - 100, draw)
    for line in def_lines:
        draw_centered_text(draw, y, line, font_text, text_color, width)
        y += 50
    
    # Пример предложения — по центру
    if example:
        y += 40
        example_text = f"\"{example}\""
        ex_lines = wrap_text(example_text, font_text, width - 100, draw)
        for line in ex_lines:
            draw_centered_text(draw, y, line, font_text, text_color, width)
            y += 45
    
    # Подпись "elfium" внизу по центру
    footer_text = "elfium"
    bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
    footer_width = bbox[2] - bbox[0]
    footer_x = (width - footer_width) // 2
    draw.text((footer_x, height - 50), footer_text, fill=footer_color, font=font_footer)
    
    # Сохраняем
    bio = BytesIO()
    bio.name = 'word.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    
    return bio

def send_word():
    word, definition, example = get_random_word()
    image_bytes = create_word_image(word, definition, example)
    bot.send_photo(CHAT_ID, photo=image_bytes)

if __name__ == '__main__':
    send_word()

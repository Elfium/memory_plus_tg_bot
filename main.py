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
    # Размеры изображения
    width = 900
    height = 700
    
    # Цвета (тёмная тема как в терминале)
    bg_color = (20, 22, 27)      # тёмно-серый фон
    accent_color = (100, 255, 100)  # зелёный акцент (как в терминале)
    text_color = (200, 200, 200)    # светлый текст
    
    # Создаём изображение
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Загружаем шрифт Monospace
    # Для GitHub Actions используем шрифт из папки fonts
    try:
        # Пытаемся загрузить моноширинный шрифт
        font_title = ImageFont.truetype("fonts/JetBrainsMono-Bold.ttf", 52)
        font_text = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 28)
        font_small = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 22)
    except:
        # Если шрифта нет, используем встроенный
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Рисуем рамку как в терминале
    draw.rectangle([10, 10, width-10, height-10], outline=accent_color, width=2)
    
    # Рисуем заголовок
    title_text = f">>> СЛОВО ДНЯ <<<"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 40), title_text, fill=accent_color, font=font_title)
    
    # Рисуем само слово (крупно)
    word_text = f"$ {word.upper()}"
    bbox = draw.textbbox((0, 0), word_text, font=font_title)
    word_width = bbox[2] - bbox[0]
    draw.text(((width - word_width) // 2, 130), word_text, fill=accent_color, font=font_title)
    
    # Разделительная линия
    draw.line(((80, 210), (width-80, 210)), fill=accent_color, width=1)
    
    # Значение
    y = 250
    draw.text((60, y), "[ значение ]", fill=accent_color, font=font_small)
    y += 40
    
    def_lines = wrap_text(definition, font_text, width - 120, draw)
    for line in def_lines:
        draw.text((80, y), line, fill=text_color, font=font_text)
        y += 40
    
    # Пример
    y += 30
    draw.text((60, y), "[ пример ]", fill=accent_color, font=font_small)
    y += 40
    
    example_text = f"\"{example}\""
    ex_lines = wrap_text(example_text, font_text, width - 120, draw)
    for line in ex_lines:
        draw.text((80, y), line, fill=text_color, font=font_text)
        y += 40
    
    # Подвал
    y = height - 60
    draw.text((60, y), "~ daily english word ~", fill=(100, 100, 120), font=font_small)
    
    # Сохраняем в BytesIO
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

def create_word_image(word, definition, example):
    # Размеры изображения
    width = 900
    height = 700
    
    # Цвета текста
    accent_color = (100, 255, 100)   # зелёный акцент
    text_color = (255, 255, 255)     # белый текст (будет виден на любом фоне)
    shadow_color = (0, 0, 0)         # чёрная тень для читаемости
    
    # Загружаем фоновое изображение
    try:
        bg = Image.open("images/background.png")
        bg = bg.resize((width, height), Image.Resampling.LANCZOS)
        img = bg.copy()
    except:
        # Если картинки нет, создаём тёмный фон
        img = Image.new('RGB', (width, height), (20, 22, 27))
    
    draw = ImageDraw.Draw(img)
    
    # Загружаем шрифты
    try:
        font_title = ImageFont.truetype("fonts/JetBrainsMono-Bold.ttf", 52)
        font_text = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 28)
        font_small = ImageFont.truetype("fonts/JetBrainsMono-Regular.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Добавляем полупрозрачную подложку для читаемости текста (опционально)
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 128))  # чёрный полупрозрачный
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Рисуем рамку
    draw.rectangle([10, 10, width-10, height-10], outline=accent_color, width=2)
    
    # Заголовок с тенью
    title_text = ">>> СЛОВО ДНЯ <<<"
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_width = bbox[2] - bbox[0]
    # Тень
    draw.text(((width - title_width) // 2 + 2, 42), title_text, fill=shadow_color, font=font_title)
    # Текст
    draw.text(((width - title_width) // 2, 40), title_text, fill=accent_color, font=font_title)
    
    # Слово
    word_text = f"$ {word.upper()}"
    bbox = draw.textbbox((0, 0), word_text, font=font_title)
    word_width = bbox[2] - bbox[0]
    draw.text(((width - word_width) // 2 + 2, 132), word_text, fill=shadow_color, font=font_title)
    draw.text(((width - word_width) // 2, 130), word_text, fill=accent_color, font=font_title)
    
    # Разделитель
    draw.line(((80, 210), (width-80, 210)), fill=accent_color, width=1)
    
    # Значение
    y = 250
    draw.text((62, y), "[ значение ]", fill=shadow_color, font=font_small)
    draw.text((60, y), "[ значение ]", fill=accent_color, font=font_small)
    y += 40
    
    def_lines = wrap_text(definition, font_text, width - 120, draw)
    for line in def_lines:
        draw.text((82, y), line, fill=shadow_color, font=font_text)
        draw.text((80, y), line, fill=text_color, font=font_text)
        y += 40
    
    # Пример
    y += 30
    draw.text((62, y), "[ пример ]", fill=shadow_color, font=font_small)
    draw.text((60, y), "[ пример ]", fill=accent_color, font=font_small)
    y += 40
    
    example_text = f"\"{example}\""
    ex_lines = wrap_text(example_text, font_text, width - 120, draw)
    for line in ex_lines:
        draw.text((82, y), line, fill=shadow_color, font=font_text)
        draw.text((80, y), line, fill=text_color, font=font_text)
        y += 40
    
    # Подвал
    y = height - 60
    draw.text((62, y), "~ daily english word ~", fill=shadow_color, font=font_small)
    draw.text((60, y), "~ daily english word ~", fill=(100, 100, 120), font=font_small)
    
    # Сохраняем
    bio = BytesIO()
    bio.name = 'word_of_the_day.png'
    img.save(bio, 'PNG')
    bio.seek(0)
    
    return bio

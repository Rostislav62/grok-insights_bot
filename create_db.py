# create_db.py
# Создаёт базу данных SQLite для хранения результатов анализа.

# Комментарии:

# sqlite3: Модуль для работы с SQLite базами.
# CREATE TABLE: Создаёт таблицу analyses с полями: ID, user_id, topic, result, timestamp.
# IF NOT EXISTS: Не создаёт таблицу, если она уже есть.

import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('insights.db')
cursor = conn.cursor()

# Таблица для анализов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        topic TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Таблица для настроек пользователя (выбранный сервис)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER PRIMARY KEY,
        selected_service TEXT DEFAULT 'xai',
        language TEXT DEFAULT 'ru'
    )
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных insights.db создана успешно!")
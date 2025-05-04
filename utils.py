# utils.py
# Утилиты для работы с xAI API и базой данных SQLite.

# Комментарии:

# analyze_text: Делает запрос к xAI API, чтобы проанализировать текст. Пока использует фиктивный URL и ключ.
# save_analysis: Сохраняет результат в базу insights.db, чтобы пользователь мог посмотреть историю.
# get_analysis_history: Вытаскивает все прошлые анализы пользователя.

import sqlite3
import logging
from services import xai, openai, huggingface, monkeylearn, watson, uclassify, textrazor
from config import DATABASE_PATH, LANGUAGE_MODE

logger = logging.getLogger(__name__)

async def analyze_text(topic, service):
    """
    Выполняет анализ текста через выбранный API.
    :param topic: Тема для анализа (например, "ИИ").
    :param service: Сервис для анализа (xai, openai, и т.д.).
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        if service == "xai":
            return await xai.analyze(topic)
        elif service == "openai":
            return await openai.analyze(topic)
        elif service == "huggingface":
            return await huggingface.analyze(topic)
        elif service == "monkeylearn":
            return await monkeylearn.analyze(topic)
        elif service == "watson":
            return await watson.analyze(topic)
        elif service == "uclassify":
            return await uclassify.analyze(topic)
        elif service == "textrazor":
            return await textrazor.analyze(topic)
        return {"summary": "Сервис не поддерживается или не активен"}
    except Exception as e:
        logger.error(f"Ошибка в analyze_text ({service}): {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}

def save_analysis(user_id, topic, result, service):
    """
    Сохраняет результат анализа в базу данных SQLite.
    :param user_id: ID пользователя Telegram.
    :param topic: Тема анализа.
    :param result: Результат анализа (текст).
    :param service: Использованный сервис.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO analyses (user_id, topic, result) VALUES (?, ?, ?)', 
                   (user_id, topic, result))
    conn.commit()
    conn.close()

def get_analysis_history(user_id):
    """
    Получает историю анализов пользователя из базы данных.
    :param user_id: ID пользователя Telegram.
    :return: Список кортежей (тема, результат, время).
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT topic, result, timestamp FROM analyses WHERE user_id = ? ORDER BY timestamp DESC', 
                   (user_id,))
    history = cursor.fetchall()
    conn.close()
    return history

def get_user_service(user_id):
    """
    Получает выбранный сервис пользователя из базы данных.
    :param user_id: ID пользователя Telegram.
    :return: Название сервиса (например, 'xai').
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT selected_service FROM user_settings WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute('INSERT OR REPLACE INTO user_settings (user_id, selected_service) VALUES (?, ?)', 
                   (user_id, 'xai'))
    conn.commit()
    conn.close()
    return 'xai'

def set_user_service(user_id, service):
    """
    Устанавливает выбранный сервис для пользователя.
    :param user_id: ID пользователя Telegram.
    :param service: Название сервиса (например, 'openai').
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_settings (user_id, selected_service) VALUES (?, ?)', 
                   (user_id, service))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    """
    Получает язык пользователя из базы данных или использует принудительный режим.
    :param user_id: ID пользователя Telegram.
    :return: Код языка ('ru' или 'en').
    """
    if LANGUAGE_MODE in ('en', 'ru'):
        return LANGUAGE_MODE  # Принудительный язык
    # Автоматический режим
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT language FROM user_settings WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute('INSERT OR REPLACE INTO user_settings (user_id, language) VALUES (?, ?)', 
                   (user_id, 'ru'))
    conn.commit()
    conn.close()
    return 'ru'

def set_user_language(user_id, language):
    """
    Устанавливает язык для пользователя.
    :param user_id: ID пользователя Telegram.
    :param language: Код языка ('ru' или 'en').
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO user_settings (user_id, language) VALUES (?, ?)', 
                   (user_id, language))
    conn.commit()
    conn.close()
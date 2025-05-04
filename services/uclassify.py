# services/uclassify.py
# Логика запросов и обработки ответов для uClassify API.
# Объяснение:

# Используем GET-запрос на https://api.uclassify.com/v1/uclassify/sentiment/classify (uClassify поддерживает GET для classify).
# Аутентификация: Authorization: Token <Read-ключ>.
# Ответ: JSON с полями positive и negative (вероятности).
# Выбираем доминирующее настроение (Positive/Negative) и его уверенность.
# Формат вывода: Sentiment: Positive (Confidence: 75.00%).

import logging
import aiohttp
from config import UCLASSIFY_API_KEY

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через uClassify API (Sentiment classifier).
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.uclassify.com/v1/uclassify/sentiment/classify",
                headers={"Authorization": f"Token {UCLASSIFY_API_KEY}", "Content-Type": "application/json"},
                json={"texts": [f"Posts about {topic} from X"]}
            ) as response:
                raw_response = await response.text()
                logger.info(f"uClassify response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        error_msg = data.get('error', 'Неизвестная ошибка')
                        return {"summary": f"uClassify API ошибка: {error_msg} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"uClassify API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                # Проверяем, что data — список с результатами
                if isinstance(data, list) and len(data) > 0:
                    positive = data[0].get("positive", 0.0)
                    negative = data[0].get("negative", 0.0)
                    sentiment = "Positive" if positive > negative else "Negative"
                    confidence = max(positive, negative)
                    return {"summary": f"Sentiment: {sentiment} (Confidence: {confidence:.2%})"}
                return {"summary": "Нет данных"}
    except Exception as e:
        logger.error(f"Ошибка в uClassify analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
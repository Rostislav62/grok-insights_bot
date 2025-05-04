# services/monkeylearn.py
# Логика запросов и обработки ответов для MonkeyLearn API.

import logging
import aiohttp
from config import MONKEYLEARN_API_KEY

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через MonkeyLearn API.
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.monkeylearn.com/v3/classifiers/cl_SentimentAnalyzer/predict/",
                headers={"Authorization": f"Token {MONKEYLEARN_API_KEY}", "Content-Type": "application/json"},
                json={"data": [f"Posts about {topic} from X"]}
            ) as response:
                raw_response = await response.text()
                logger.info(f"MonkeyLearn response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        error_msg = data.get('error', 'Неизвестная ошибка')
                        return {"summary": f"MonkeyLearn API ошибка: {error_msg} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"MonkeyLearn API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                # Проверяем, что data — список с результатами
                if isinstance(data, list) and len(data) > 0:
                    classification = data[0].get("classifications", [{}])[0]
                    sentiment = classification.get("tag_name", "Неизвестно")
                    confidence = classification.get("confidence", 0.0)
                    return {"summary": f"Sentiment: {sentiment} (Confidence: {confidence:.2%})"}
                return {"summary": "Нет данных"}
    except Exception as e:
        logger.error(f"Ошибка в MonkeyLearn analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
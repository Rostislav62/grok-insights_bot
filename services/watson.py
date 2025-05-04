# services/watson.py
# Логика запросов и обработки ответов для IBM Watson Natural Language Understanding API.
# Объяснение:

# Используем endpoint v1/analyze с версией 2022-04-07.
# Аутентификация через BasicAuth с префиксом apikey.
# Запрашиваем анализ настроений (sentiment) и ключевых слов (keywords).
# Форматируем вывод как Sentiment: positive (Score: 0.95)\nKeywords: AI, machine learning.
# Ошибки логируются с HTTP-кодом.


import logging
import aiohttp
from config import WATSON_API_KEY, WATSON_URL

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через IBM Watson NLU API.
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{WATSON_URL}/v1/analyze?version=2022-04-07",
                headers={"Content-Type": "application/json"},
                auth=aiohttp.BasicAuth("apikey", WATSON_API_KEY),
                json={
                    "text": f"Posts about {topic} from X",
                    "features": {
                        "sentiment": {},
                        "keywords": {}
                    }
                }
            ) as response:
                raw_response = await response.text()
                logger.info(f"Watson response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        error_msg = data.get('error', 'Неизвестная ошибка')
                        return {"summary": f"Watson API ошибка: {error_msg} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"Watson API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                sentiment = data.get("sentiment", {}).get("document", {}).get("label", "Неизвестно")
                score = data.get("sentiment", {}).get("document", {}).get("score", 0.0)
                keywords = [kw.get("text", "") for kw in data.get("keywords", [])]
                summary = f"Sentiment: {sentiment} (Score: {score:.2f})"
                if keywords:
                    summary += f"\nKeywords: {', '.join(keywords)}"
                return {"summary": summary}
    except Exception as e:
        logger.error(f"Ошибка в Watson analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
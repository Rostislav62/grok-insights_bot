# services/openai.py
# Логика запросов и обработки ответов для OpenAI API.

import logging
import aiohttp
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через OpenAI API.
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are an AI analyst. Analyze posts about a topic and provide a summary with sentiment, keywords, and trends."},
                        {"role": "user", "content": f"Simulate analyzing posts about {topic} from X"}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 200
                }
            ) as response:
                raw_response = await response.text()
                logger.info(f"OpenAI response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        return {"summary": f"OpenAI API ошибка: {data.get('error', {}).get('message', 'Неизвестная ошибка')} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"OpenAI API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                return {"summary": data.get("choices", [{}])[0].get("message", {}).get("content", "Нет данных")}
    except Exception as e:
        logger.error(f"Ошибка в OpenAI analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
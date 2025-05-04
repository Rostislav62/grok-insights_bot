# services/xai.py
# Логика запросов и обработки ответов для xAI API.

import logging
import aiohttp
from config import XAI_API_KEY

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через xAI API.
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.x.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {XAI_API_KEY}"},
                json={
                    "model": "grok-beta",
                    "messages": [
                        {"role": "system", "content": "You are an AI analyst. Analyze posts about a topic from X and provide a summary with sentiment, keywords, and trends."},
                        {"role": "user", "content": f"Analyze posts about {topic} from X"}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 200
                }
            ) as response:
                raw_response = await response.text()
                logger.info(f"xAI response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        code = data.get('code', 'Неизвестный код')
                        error_msg = data.get('error', 'Неизвестная ошибка')
                        full_error = f"{code}. {error_msg}"
                        return {"summary": f"xAI API ошибка: {full_error} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"xAI API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                return {"summary": data.get("choices", [{}])[0].get("message", {}).get("content", "Нет данных")}
    except Exception as e:
        logger.error(f"Ошибка в xAI analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
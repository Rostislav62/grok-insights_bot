# services/huggingface.py
# Логика запросов и обработки ответов для Hugging Face Inference API.

# Объяснение:
# Используем модель distilbert-base-uncased-finetuned-sst-2-english для анализа настроений.
# Запрос отправляется на https://api-inference.huggingface.co/models/<model>.
# Ответ обрабатывается как JSON, возвращаем настроение (POSITIVE/NEGATIVE) и уверенность.
# Ошибки логируются и отображаются с HTTP-кодом.

import logging
import aiohttp
from config import HF_API_KEY

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через Hugging Face Inference API.
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                json={"inputs": f"Posts about {topic} from X"}
            ) as response:
                raw_response = await response.text()
                logger.info(f"Hugging Face response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        error_msg = data.get('error', 'Неизвестная ошибка')
                        return {"summary": f"Hugging Face API ошибка: {error_msg} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"Hugging Face API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                # Проверяем, что data — список списков
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    # Выбираем результат с максимальным score
                    results = data[0]
                    if not results:
                        return {"summary": "Нет данных"}
                    best_result = max(results, key=lambda x: x.get("score", 0.0))
                    sentiment = best_result.get("label", "Неизвестно")
                    score = best_result.get("score", 0.0)
                    return {"summary": f"Sentiment: {sentiment} (Confidence: {score:.2%})"}
                return {"summary": "Неверный формат ответа от Hugging Face"}
    except Exception as e:
        logger.error(f"Ошибка в Hugging Face analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
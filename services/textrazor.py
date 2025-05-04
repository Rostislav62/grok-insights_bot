# services/textrazor.py
# Логика запросов и обработки ответов для TextRazor API.
# Объяснение:

# Endpoint: https://api.textrazor.com/.
# Аутентификация: Заголовок x-textrazor-key.
# Тело запроса: Формат application/x-www-form-urlencoded, с полями text и extractors (запрашиваем sentiment и entities).
# Ответ: JSON с полем sentiment.score (от -1 до 1) и списком entities.
# Формат вывода: Sentiment: Positive\nEntities: AI, machine learning.

import logging
import aiohttp
from config import TEXTRAZOR_API_KEY

logger = logging.getLogger(__name__)

async def analyze(topic):
    """
    Выполняет анализ текста через TextRazor API (Sentiment и Entities).
    :param topic: Тема для анализа (например, "ИИ").
    :return: Словарь с результатом {"summary": "текст"}.
    """
    try:
        # Более развёрнутый текст для анализа
        input_text = (
            f"Users on X are buzzing with excitement about {topic} advancements, celebrating breakthroughs in "
            f"machine learning, deep learning, and automation. Many posts praise how {topic} enhances productivity, "
            f"drives innovation, and opens new career paths in tech. However, some users voice serious concerns, "
            f"warning that {topic} could lead to widespread job losses, ethical dilemmas, and privacy issues. "
            f"The debate is intense, with passionate arguments for and against {topic}'s impact. Supporters call it "
            f"a game-changer, while critics fear it may disrupt society."
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.textrazor.com/",
                headers={
                    "x-textrazor-key": TEXTRAZOR_API_KEY,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={
                    "text": input_text,
                    "extractors": "sentiment,entities",
                    "language": "eng",
                    "sentiment_rules": "true"
                }
            ) as response:
                raw_response = await response.text()
                logger.info(f"TextRazor response (HTTP {response.status}): {raw_response}")
                if response.status != 200:
                    try:
                        data = await response.json()
                        error_msg = data.get('error', 'Неизвестная ошибка')
                        return {"summary": f"TextRazor API ошибка: {error_msg} (HTTP {response.status})"}
                    except ValueError:
                        return {"summary": f"TextRazor API ошибка: {raw_response} (HTTP {response.status})"}
                data = await response.json()
                response_data = data.get("response", {})
                sentiment = response_data.get("sentiment", {}).get("score", None)
                if isinstance(sentiment, (int, float)):
                    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"
                else:
                    sentiment_label = "Недостаточно данных для анализа настроений"
                entities = [entity.get("entityId", "") for entity in response_data.get("entities", [])]
                summary = f"Sentiment: {sentiment_label}"
                if entities:
                    summary += f"\nEntities: {', '.join(entities)}"
                return {"summary": summary}
    except Exception as e:
        logger.error(f"Ошибка в TextRazor analyze: {str(e)}")
        return {"summary": f"Ошибка: {str(e)}"}
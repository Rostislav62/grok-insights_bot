# config.py
# Загрузка токена API
# API_TOKEN = '7148692650:AAGgk9MkQJKicsPsK3GD-QhTku5u1XILIfQ'
# API_TOKEN = '7160813775:AAEMBRCqmujyumtZTXTwEEswcPGLNu7iOdY'
# API_TOKEN = '7735415258:AAFz18cHUdS1UiVhgPiHi0WC_yKKsl95GFg'
# You will find it at t.me/ZooQuizBot2025_bot. You can now add a description,
# about section and profile picture for your bot, see /help for a list of commands.
# By the way, when you('ve finished creating your cool bot, ping our Bot Support if you want a better username for it. '
#                      'Just make sure the bot is fully operational before you do this.)
#
# Use this token to access the HTTP API:
# 7735415258:AAFz18cHUdS1UiVhgPiHi0WC_yKKsl95GFg
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api
# URL https://api.x.ai/v1/analyze

# Start by making your first request to the chat completions API:
# curl https://api.x.ai/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -H "Authorization: Bearer xai-NSJhJJotgWgKWNsZBRYHFszBJOB4vLhMGuUBdBlfOxzOxu7bngfwlig3qRDzhdA44KLUwjUlL1h61IkR" \
#   -d '{
#   "messages": [
#     {
#       "role": "system",
#       "content": "You are a test assistant."
#     },
#     {
#       "role": "user",
#       "content": "Testing. Just say hi and hello world and nothing else."
#     }
#   ],
#   "model": "grok-3-latest",
#   "stream": false,
#   "temperature": 0
# }'


BOT_TOKEN = "your_new_bot_token"  # Токен от BotFather
XAI_API_KEY = "xai-placeholder_key"  # Заглушка для xAI
OPENAI_API_KEY = "sk-placeholder_openai_key"  # Заглушка для OpenAI
HF_API_KEY = "hf-placeholder_huggingface_key"  # Заглушка для Hugging Face
MONKEYLEARN_API_KEY = "MonkeyLearn-098q3098-2039845key"  # MonkeyLearn (заглушка)
WATSON_API_KEY = "IBM_Watsonaqwepopweriq-0werkey"  # IBM Watson (заглушка)
WATSON_URL = ""  # IBM Watson URL (заглушка)
UCLASSIFY_API_KEY = "uc-placeholder_uclassify_key"  # Заглушка для uClassify
TEXTRAZOR_API_KEY = "tr-placeholder_textrazor_key"  # Заглушка для TextRazor
DATABASE_PATH = "insights.db"  # Путь к базе данных

# Режим языка: "auto" (по настройкам пользователя), "en" (принудительно английский), "ru" (принудительно русский)
LANGUAGE_MODE = "auto"

# Список доступных сервисов
AVAILABLE_SERVICES = {
    "xai": {"name": "xAI", "active": True},
    "openai": {"name": "OpenAI", "active": True},
    "huggingface": {"name": "Hugging Face", "active": True},
    "monkeylearn": {"name": "MonkeyLearn", "active": True},
    "watson": {"name": "IBM Watson", "active": True},
    "uclassify": {"name": "uClassify", "active": True},
    "textrazor": {"name": "TextRazor", "active": True}
}
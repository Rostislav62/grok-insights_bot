# main.py
# Основной файл для запуска Grok Insights Bot.
# Python 3.8.10
# для корректной работы этого бота я загнузил эти пакеты
# pip install aiogram==2.21 aiohttp==3.8.1
# содержит только тот код который нужен для старта и управления ботом.
# 

# Комментарии:

# logging: Помогает видеть, что происходит (ошибки, старт бота).
# Bot, Dispatcher: Основные объекты aiogram для работы бота.
# MemoryStorage: Хранит состояния (например, текущую тему анализа).
# register_handlers: Подключает команды и кнопки из handlers.py.
# start_polling: Запускает бота, чтобы он слушал сообщения.


import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import BOT_TOKEN
from handlers import register_handlers

# Настраиваем логирование для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализируем бота с токеном
bot = Bot(token=BOT_TOKEN)
# Создаём хранилище состояний в памяти
storage = MemoryStorage()
# Создаём диспетчер для обработки команд
dp = Dispatcher(bot, storage=storage)

# Регистрируем обработчики
register_handlers(dp)

if __name__ == '__main__':
    # Запускаем бота
    logger.info("Starting Grok Insights Bot...")
    executor.start_polling(dp, skip_updates=True)
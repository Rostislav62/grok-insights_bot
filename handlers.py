# handlers.py
# Обработчики команд и кнопок для Grok Insights Bot.

# Комментарии:

# AnalysisStates: Хранит состояние, чтобы знать, какую тему повторять.
# get_analysis_keyboard: Создаёт кнопки "Повторить", "Поделиться", "История".
# start: Приветствует пользователя и объясняет, как начать.
# analyze_command: Запрашивает анализ и показывает отчёт.
# repeat_analysis, share_analysis, view_history: Обрабатывают кнопки.
# register_handlers: Связывает команды и кнопки с функциями.

import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AVAILABLE_SERVICES, LANGUAGE_MODE
from utils import analyze_text, save_analysis, get_analysis_history, get_user_service, set_user_service, get_user_language

# Настраиваем логирование для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Локализация сообщений
MESSAGES = {
    "ru": {
        "start": "Привет! Я Grok Insights Bot, умею анализировать посты в X. Введи тему: /analyze <тема> (например, /analyze ИИ)",
        "select_service": "Выбери сервис для анализа:",
        "service_selected": "Выбран сервис: {service}",
        "no_topic": "Пожалуйста, укажи тему! Например: /analyze ИИ",
        "analyzing": "Анализирую посты в X по теме '{topic}' с помощью {service}...",
        "report": "Отчёт по теме '{topic}' ({service}):\n{summary}",
        "history_empty": "История анализов пуста!",
        "history": "История анализов:\n",
        "history_item": "- {timestamp}: {topic}\n  Результат: {result}\n",
        "help": (
            "Grok Insights Bot — это бот для анализа постов в X.\n\n"
            "Команды:\n"
            "/start — Начать\n"
            "/analyze <тема> — Проанализировать тему\n"
            "/select_service — Выбрать сервис (xAI, OpenAI, и др.)\n"
            "/history — Показать историю анализов\n"
            "/help — Показать это сообщение\n\n"
            "Поддерживаемые языки: Русский, Английский\n"
        ),
        "repeat": "Повторить",
        "share": "Поделиться",
        "history_button": "История"
    },
    "en": {
        "start": "Hi! I'm Grok Insights Bot, I analyze X posts. Enter a topic: /analyze <topic> (e.g., /analyze AI)",
        "select_service": "Choose a service for analysis:",
        "service_selected": "Selected service: {service}",
        "no_topic": "Please specify a topic! E.g., /analyze AI",
        "analyzing": "Analyzing X posts on '{topic}' using {service}...",
        "report": "Report for topic '{topic}' ({service}):\n{summary}",
        "history_empty": "Analysis history is empty!",
        "history": "Analysis history:\n",
        "history_item": "- {timestamp}: {topic}\n  Result: {result}\n",
        "help": (
            "Grok Insights Bot analyzes X posts.\n\n"
            "Commands:\n"
            "/start — Start\n"
            "/analyze <topic> — Analyze a topic\n"
            "/select_service — Choose a service (xAI, OpenAI, etc.)\n"
            "/history — Show analysis history\n"
            "/help — Show this message\n\n"
            "Supported languages: Russian, English\n"
        ),
        "repeat": "Repeat",
        "share": "Share",
        "history_button": "History"
    }
}

# Класс для управления состояниями
class AnalysisStates(StatesGroup):
    waiting_for_topic = State()

def get_analysis_keyboard(language):
    """
    Создаёт клавиатуру с кнопками после анализа.
    :param language: Код языка ('ru' или 'en').
    :return: InlineKeyboardMarkup с кнопками.
    """
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(MESSAGES[language]["repeat"], callback_data="repeat_analysis"),
        InlineKeyboardButton(MESSAGES[language]["share"], callback_data="share_analysis")
    )
    markup.add(InlineKeyboardButton(MESSAGES[language]["history_button"], callback_data="view_history"))
    return markup

def get_service_keyboard():
    """
    Создаёт клавиатуру с доступными сервисами.
    :return: InlineKeyboardMarkup с кнопками сервисов.
    """
    markup = InlineKeyboardMarkup()
    for service_id, service in AVAILABLE_SERVICES.items():
        markup.add(InlineKeyboardButton(
            service["name"],
            callback_data=f"select_service_{service_id}",
            disabled=not service["active"]
        ))
    return markup

async def start(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /start, отправляет приветственное сообщение.
    :param message: Сообщение от пользователя.
    :param state: Состояние FSM.
    """
    await state.finish()  # Сбрасываем состояние
    language = get_user_language(message.from_user.id)
    logger.info(f"User {message.from_user.id} started bot, language: {language}")
    await message.reply(MESSAGES[language]["start"])

async def select_service_command(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /select_service, показывает доступные сервисы.
    :param message: Сообщение от пользователя.
    :param state: Состояние FSM.
    """
    await state.finish()  # Сбрасываем состояние
    language = get_user_language(message.from_user.id)
    logger.info(f"User {message.from_user.id} requested service selection")
    await message.reply(MESSAGES[language]["select_service"], reply_markup=get_service_keyboard())

async def select_service_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор сервиса через кнопку.
    :param callback_query: Callback от кнопки.
    :param state: Состояние FSM.
    """
    await state.finish()  # Сбрасываем состояние
    language = get_user_language(callback_query.from_user.id)
    service_id = callback_query.data.replace("select_service_", "")
    if service_id in AVAILABLE_SERVICES and AVAILABLE_SERVICES[service_id]["active"]:
        set_user_service(callback_query.from_user.id, service_id)
        await callback_query.message.reply(
            MESSAGES[language]["service_selected"].format(service=AVAILABLE_SERVICES[service_id]["name"])
        )
    else:
        await callback_query.message.reply("Этот сервис пока не активен!" if language == "ru" else "This service is not active yet!")
    await callback_query.answer()

async def analyze_command(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /analyze, запрашивает анализ и показывает результат.
    :param message: Сообщение с командой /analyze.
    :param state: Состояние для сохранения темы.
    """
    language = get_user_language(message.from_user.id)
    topic = message.text.replace('/analyze ', '').strip()
    if not topic:
        await message.reply(MESSAGES[language]["no_topic"])
        return
    await state.update_data(topic=topic)
    service = get_user_service(message.from_user.id)
    await message.reply(MESSAGES[language]["analyzing"].format(topic=topic, service=AVAILABLE_SERVICES[service]["name"]))
    result = await analyze_text(topic, service)
    summary = result.get('summary', 'Нет данных')
    save_analysis(message.from_user.id, topic, summary, service)
    await message.reply(
        MESSAGES[language]["report"].format(topic=topic, service=AVAILABLE_SERVICES[service]["name"], summary=summary),
        reply_markup=get_analysis_keyboard(language)
    )
    await AnalysisStates.waiting_for_topic.set()

async def repeat_analysis(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Повторяет анализ по текущей теме.
    :param callback_query: Callback от кнопки.
    :param state: Состояние с темой.
    """
    language = get_user_language(callback_query.from_user.id)
    data = await state.get_data()
    topic = data.get('topic')
    if not topic:
        await callback_query.message.reply(MESSAGES[language]["no_topic"])
        return
    service = get_user_service(callback_query.from_user.id)
    result = await analyze_text(topic, service)
    summary = result.get('summary', 'Нет данных')
    save_analysis(callback_query.from_user.id, topic, summary, service)
    await callback_query.message.reply(
        MESSAGES[language]["report"].format(topic=topic, service=AVAILABLE_SERVICES[service]["name"], summary=summary),
        reply_markup=get_analysis_keyboard(language)
    )
    await callback_query.answer()

async def share_analysis(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Позволяет поделиться отчётом через Telegram.
    :param callback_query: Callback от кнопки.
    :param state: Состояние с темой.
    """
    language = get_user_language(callback_query.from_user.id)
    data = await state.get_data()
    topic = data.get('topic')
    if not topic:
        await callback_query.message.reply(MESSAGES[language]["no_topic"])
        return
    await callback_query.message.reply(
        MESSAGES[language]["share"],
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(
                MESSAGES[language]["share"],
                url=f"https://t.me/share/url?url=Analysis on {topic}"
            )
        )
    )
    await callback_query.answer()

async def view_history(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Показывает историю анализов пользователя.
    :param callback_query: Callback от кнопки.
    :param state: Состояние FSM.
    """
    await state.finish()  # Сбрасываем состояние
    language = get_user_language(callback_query.from_user.id)
    history = get_analysis_history(callback_query.from_user.id)
    if not history:
        await callback_query.message.reply(MESSAGES[language]["history_empty"])
        return
    response = MESSAGES[language]["history"]
    for topic, result, timestamp in history:
        response += MESSAGES[language]["history_item"].format(timestamp=timestamp, topic=topic, result=result)
    await callback_query.message.reply(response)
    await callback_query.answer()

async def help_command(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /help, показывает инструкции.
    :param message: Сообщение от пользователя.
    :param state: Состояние FSM.
    """
    await state.finish()  # Сбрасываем состояние
    language = get_user_language(message.from_user.id)
    logger.info(f"User {message.from_user.id} requested help, language: {language}")
    await message.reply(MESSAGES[language]["help"])

def register_handlers(dp: Dispatcher):
    """
    Регистрирует все обработчики команд и кнопок.
    :param dp: Dispatcher бота.
    """
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(select_service_command, commands=['select_service'], state='*')
    dp.register_message_handler(analyze_command, commands=['analyze'], state='*')
    dp.register_message_handler(help_command, commands=['help'], state='*')
    dp.register_callback_query_handler(select_service_callback, lambda c: c.data.startswith('select_service_'), state='*')
    dp.register_callback_query_handler(repeat_analysis, lambda c: c.data == 'repeat_analysis', 
                                      state=AnalysisStates.waiting_for_topic)
    dp.register_callback_query_handler(share_analysis, lambda c: c.data == 'share_analysis', 
                                      state=AnalysisStates.waiting_for_topic)
    dp.register_callback_query_handler(view_history, lambda c: c.data == 'view_history', state='*')
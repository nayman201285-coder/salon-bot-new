import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=TOKEN)

# Создаем Flask приложение
app = Flask(__name__)

# Создаем приложение Telegram
telegram_app = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update, context):
    await update.message.reply_text('👋 Привет! Я бот для салона красоты!')

# Обработчик текстовых сообщений
async def echo(update, context):
    await update.message.reply_text(f'Ты написал: {update.message.text}')

# Добавляем обработчики
telegram_app.add_handler(CommandHandler('start', start))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# Инициализируем приложение
import asyncio
asyncio.run(telegram_app.initialize())

# Вебхук для приема обновлений
@app.route('/webhook', methods=['POST'])
def webhook():
    """Принимает обновления от Telegram"""
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(telegram_app.process_update(update))
    return 'OK', 200

# Главная страница для проверки
@app.route('/')
def index():
    return 'Bot is running!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
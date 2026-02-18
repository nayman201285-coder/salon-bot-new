import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(token=TOKEN)

app = Flask(__name__)

# Создаем диспетчер для старой версии
dispatcher = Dispatcher(bot, None, workers=0)

def start(update, context):
    update.message.reply_text('👋 Привет! Я бот для салона красоты!')

def echo(update, context):
    update.message.reply_text(f'Ты написал: {update.message.text}')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK', 200

@app.route('/')
def index():
    return 'Bot is running!', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
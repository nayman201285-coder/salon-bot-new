from flask import Flask, request, Response
import requests
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Внутренний IP твоего сервера Oracle (НЕ МЕНЯТЬ!)
ORACLE_SERVER = "http://10.0.1.87:10000"

@app.route('/webhook', methods=['POST'])
def proxy():
    """Принимает вебхук от Telegram и отправляет в Oracle"""
    try:
        # Получаем данные от Telegram
        data = request.get_json()
        logger.info(f"🔥 Получен запрос от Telegram, пересылаю в Oracle")
        
        # Отправляем в Oracle
        response = requests.post(
            f"{ORACLE_SERVER}/webhook",
            json=data,
            timeout=10
        )
        
        # Возвращаем ответ Telegram
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'application/json')
        )
    except Exception as e:
        logger.error(f"❌ Ошибка: {e}")
        return "OK", 200  # Telegram требует 200 даже при ошибках

@app.route('/')
def index():
    return 'Render Proxy is running!', 200

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

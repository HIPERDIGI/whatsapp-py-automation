# webhook_receiver.py
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from google_sheets import update_interest_status

load_dotenv()

app = Flask(__name__)

SHEET_NAME = os.getenv('SHEET_NAME')
SHEET_PAGE = os.getenv('SHEET_PAGE')
SHEET_LOG_PAGE = os.getenv('SHEET_LOG_PAGE')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    print("📥 Dados recebidos:", data)

    phone = data.get('phone')

    # Para botões clicados
    button_response = data.get('buttonResponse')

    # Para mensagens digitadas
    message = None
    if 'message' in data and isinstance(data['message'], dict):
        message = data['message'].get('text')

    user_reply = button_response or message

    if phone and user_reply:
        # Atualiza a planilha: você pode adaptar para buscar e escrever na linha certa
        update_interest_status(phone, user_reply)
        return jsonify({"status": "success"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

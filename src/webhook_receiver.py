# webhook_receiver.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from google_sheets import update_interest_status
from whatsapp_sender import send_text_message

load_dotenv()

app = Flask(__name__)

NOTIFY_PHONE = os.getenv('NOTIFY_PHONE')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    phone = data.get('phone')  # Número de quem respondeu
    button_response = data.get('buttonResponse')

    if button_response == "Não tenho interesse ☹️":
        # Atualizar a planilha
        update_interest_status(phone, "Não tenho interesse")

        # Enviar mensagem para o telefone de notificação
        message = f"{phone} marcou 'não tenho interesse'."
        send_text_message(NOTIFY_PHONE, message)

        return jsonify({"status": "success"}), 200

    return jsonify({"status": "ignored"}), 200

if __name__ == "__main__":
    app.run(port=5000)

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from google_sheets import update_user_reply, listar_telefones_e_status

load_dotenv()

app = Flask(__name__)

SHEET_NAME = os.getenv('SHEET_NAME')
SHEET_PAGE = os.getenv('SHEET_PAGE')
SHEET_LOG_PAGE = os.getenv('SHEET_LOG_PAGE')

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"status": "error", "message": "JSON inválido"}), 400

    print("📥 Dados recebidos:", data)

    phone = data.get('phone')
    button_response = data.get('buttonResponse')
    message = data.get('message', {}).get('text') if isinstance(data.get('message'), dict) else None

    user_reply = button_response or message

    if phone and user_reply:
        try:
            update_user_reply(phone, user_reply)
            return jsonify({"status": "success"}), 200
        except Exception as e:
            print(f"Erro ao atualizar planilha: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "ignored"}), 200

@app.route('/', methods=['GET'])
def index():
    return "Webhook ativo", 200

if __name__ == "__main__":
    # listar_telefones_e_status()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

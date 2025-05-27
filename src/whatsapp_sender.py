import requests
import os
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv('ZAPI_BASE_URL')
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')

HEADERS = {
    "Client-Token": CLIENT_TOKEN,
    "Content-Type": "application/json"
}


def send_message_btn(phone_number: str):
    url = f"{ZAPI_BASE_URL}/send-button-actions"

    payload = {
        "phone": phone_number,
        "message": "🤖 CAPTURA INTELIGENTE com IA\n📲 Basta uma foto da folha de resposta e pronto:\n✔️ Correção automática do gabarito\n✔️ Resultados por aluno, turma e conteúdo\n📊 Análises instantâneas para tomada de decisão\n\n🚀 Transforme a forma como sua escola avalia!\n",
        "title": "📌 Sua escola ainda corrige provas manualmente? Com o Zoom Educa, você corrige avaliações em segundos, usando apenas o celular!\n",
        "footer": "🔗 Saiba mais: zoomeduca.com.br/saiba-mais/captura-de-folhas",
        "buttonActions": [
            {
                "id": "1",
                "type": "URL",
                "url": "https://api.whatsapp.com/send?phone=5586999812204&text=Olá%2C+gostaria+de+saber+mais+sobre+o+zoom+educa%21",
                "label": "Tenho interesse 😁"
            },
            {
                "id": "2",
                "type": "URL",
                "url": "https://wa.me/5586999856371",
                "label": "Não tenho interesse ☹️"
            },
        ]
    }

    send_request(url, payload, phone_number)


def send_image(phone_number: str):
    url = f"{ZAPI_BASE_URL}/send-image"

    payload = {
        "phone": phone_number,
        "image": "https://zoomeduca.com.br/gestor_2705.jpeg"
    }

    send_request(url, payload, phone_number)


def send_request(url: str, payload: dict, phone_number: str):

    response = requests.post(url, headers=HEADERS, json=payload)

    print("Status Code:", response.status_code)

    try:
        # print("Response JSON:", response.json())
        pass
    except Exception:
        print("Response Text:", response.text)

    if response.status_code == 200:
        print(f"✅ Mensagem enviada para {phone_number}")
    else:
        print(
            f"❌ Erro ao enviar mensagem para {phone_number}. Status: {response.status_code}")

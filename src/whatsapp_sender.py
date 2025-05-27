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
    url = f"{ZAPI_BASE_URL}/send-button-list"

    payload = {
        "phone": phone_number,
        "message": "Com o Zoom Educa, sua escola ganha uma visão precisa do desempenho dos alunos como se estivessem fazendo o ENEM de verdade!\n📊 Simulação REAL com base nas notas da escola\n🎓 Veja quem passaria no SISU, ProUni ou FIES\n🚀 Descubra os alunos com maior chance de aprovação\n🛠️ Identifique quem precisa de reforço e em que áreas!",
        "title": "🎯 Você sabia que é possível descobrir agora mesmo quais alunos da sua escola já estariam APROVADOS no ENEM?",
        "footer": "💡 Transforme suas avaliações em dados estratégicos e impulsione seus resultados!",
        "buttonActions": [
            {
                "id": "1",
                "type": "URL",
                "url": "https://zoomeduca.com.br",
                "label": "Visite nosso site"
            },
            {
                "id": "2",
                "type": "URL",
                "url": "https://wa.me/5586999812204",
                "label": "Fale com um consultor"
            },
        ]
    }

    send_request(url, payload, phone_number)


def send_image(phone_number: str):
    url = f"{ZAPI_BASE_URL}/send-image"

    payload = {
        "phone": phone_number,
        "image": "https://zoomeduca.com.br/what-feedback.jpeg"
    }

    send_request(url, payload, phone_number)


def send_request(url: str, payload: dict, phone_number: str):

    response = requests.post(url, headers=HEADERS, json=payload)

    print("Status Code:", response.status_code)

    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)

    if response.status_code == 200:
        print(f"✅ Mensagem enviada para {phone_number}")
    else:
        print(
            f"❌ Erro ao enviar mensagem para {phone_number}. Status: {response.status_code}")

import requests
import os
from dotenv import load_dotenv
from google_sheets import log_sent_message

load_dotenv()

ZAPI_BASE_URL = os.getenv('ZAPI_BASE_URL')
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')
SHEET_NAME = os.getenv('SHEET_NAME')
SHEET_LOG_PAGE = os.getenv('SHEET_LOG_PAGE')

HEADERS = {
    "Client-Token": CLIENT_TOKEN,
    "Content-Type": "application/json"
}

def send_text_message(phone_number: str, message: str):
    url = f"{ZAPI_BASE_URL}/send-text"
    payload = {
        "phone": phone_number,
        "message": message
    }
    return send_request(url, payload, phone_number)

def send_message_btn(phone_number: str):
    url = f"{ZAPI_BASE_URL}/send-button-actions"

    payload = {
        "phone": phone_number,
        "message": "📈 O gráfico na tela? É só uma amostra do poder da Zoom Educa:\n💡 Acompanhe o desempenho por série, por turma ou por aluno.\n ⚙️ Automatize a correção das provas.\n 📊 Tome decisões pedagógicas com base em dados reais. \n\n🧠 Mais que uma plataforma, um aliado estratégico na gestão escolar. Deixe o retrabalho no passado e abrace a eficiência!\n",
        "title": "📱✨ Seu boletim de resultados em tempo real, direto na palma da mão!\n",
        "footer": "🔗 Descubra como:\n www.zoomeduca.com.br",
        "buttonActions": [
            {
                "id": "1",
                "type": "URL",
                "url": "https://api.whatsapp.com/send?phone=5586999812204&text=Ol%C3%A1%2C%20gostaria%20de%20saber%20mais%20sobre%20o%20zoom%20educa",
                # uso do % para separar as palavras da mensagem é funcional
                "url": "https://api.whatsapp.com/send?phone=5586999812204&text=Ol%C3%A1%2C%20gostaria%20de%20saber%20mais%20sobre%20o%20zoom%20educa",
                "label": "Tenho interesse 😁"
            },
            {
                "id": "2",
                "type": "REPLY",
                "type": "REPLY",
                "label": "Não tenho interesse ☹️"
            },
        ]
    }

    return send_request(url, payload, phone_number)


def send_image(phone_number: str):
    url = f"{ZAPI_BASE_URL}/send-image"

    payload = {
        "phone": phone_number,
        "image": "https://zoomeduca.com.br/mkt_020625.jpeg"
        # "image": "https://zoomeduca.com.br/gestor_2705.jpeg"
    }

    return send_request(url, payload, phone_number)

def send_all_messages(phone_number: str):
    success_image = send_image(phone_number)
    success_text = send_message_btn(phone_number)

    if success_image and success_text:
        log_sent_message(phone_number, "Enviado", SHEET_NAME, SHEET_LOG_PAGE)
    else:
        print(f"⚠️ Nem todas as mensagens foram enviadas para {phone_number}. Nenhum log registrado.")


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
        return True
        
    else:
        print(
            f"❌ Erro ao enviar mensagem para {phone_number}. Status: {response.status_code}")
        return False

import time
from google_sheets import get_phone_numbers
from whatsapp_sender import send_message_btn, send_image
import os
from dotenv import load_dotenv

load_dotenv()

SHEET_NAME = os.getenv('SHEET_NAME')
SHEET_PAGE = os.getenv('SHEET_PAGE')


def main():
    print("🔗 Buscando números da planilha...")
    phone_numbers = get_phone_numbers(SHEET_NAME, SHEET_PAGE)

    print(f"Encontrados {len(phone_numbers)} números.")

    for phone in phone_numbers:
        send_image(phone)
        send_message_btn(phone)
        time.sleep(2)  # Delay entre envios


if __name__ == "__main__":
    main()

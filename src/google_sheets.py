import os
import datetime
import pickle
import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv('ZAPI_BASE_URL')
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')
SHEET_NAME = os.getenv('SHEET_NAME')
SHEET_PAGE = os.getenv('SHEET_PAGE')
SHEET_LOG_PAGE = os.getenv('SHEET_LOG_PAGE')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]


def authenticate_google():
    creds = None
    token_path = 'credentials/token.pickle'
    creds_path = 'credentials/credentials.json'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    client = gspread.authorize(creds)
    return client


def get_phone_numbers(sheet_name: str, sheet_page: str):
    client = authenticate_google()
    sheet = client.open(sheet_name).worksheet(sheet_page)

    header = sheet.range('A1:Z1')
    headers = [cell.value.strip().lower()
               for cell in header if cell.value.strip() != '']

    try:
        col_index = next(i for i, h in enumerate(
            headers) if 'telefone' in h) + 1
    except StopIteration:
        raise Exception(
            'Coluna com cabeçalho contendo "Telefone" não encontrada.')

    phone_numbers = sheet.col_values(col_index)
    phone_numbers = phone_numbers[1:]  # Ignorar cabeçalho

    return [p.strip() for p in phone_numbers if p.strip() and p.strip().isdigit()]


def log_sent_message(phone_number: str, status: str, sheet_name: str, sheet_page: str):
    client = authenticate_google()
    sheet = client.open(sheet_name).worksheet(sheet_page)

    header_row = sheet.row_values(1)

    try:
        phone_col = header_row.index('Telefone') + 1
        status_col = header_row.index('Status') + 1
        datetime_col = header_row.index('Data/Hora de Envio') + 1
    except ValueError as e:
        raise Exception(f"Erro: Cabeçalho não encontrado ou incorreto - {e}")

    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    next_row = len(sheet.col_values(1)) + 1

    sheet.update_cell(next_row, phone_col, phone_number)
    sheet.update_cell(next_row, status_col, status)
    sheet.update_cell(next_row, datetime_col, now)


def update_user_reply(phone_number: str, reply_message: str):
    client = authenticate_google()
    sheet = client.open(SHEET_NAME).worksheet(SHEET_LOG_PAGE)

    data = sheet.get_all_records()
    header = sheet.row_values(1)

    try:
        message_col = header.index('Mensagem') + 1
        message_time_col = header.index('Data/Hora Mensagem Recebida') + 1
    except ValueError as e:
        print(f"Erro: cabeçalho não encontrado - {e}")
        return

    row_number = None
    for idx, row in reversed(list(enumerate(data, start=2))):
        telefone = str(row.get('Telefone', '')).strip().replace(
            ' ', '').replace('+', '')
        status = str(row.get('Status', '')).strip().lower()
        telefone_clean = phone_number.strip().replace(' ', '').replace('+', '')
        print(f"telefone clean: {telefone_clean}")
        print(f"status: {status}")

        if telefone == telefone_clean and status == 'enviado':
            row_number = idx
            break

    if not row_number:
        print(f"Telefone {phone_number} com status 'Enviado' não encontrado.")
        return
    
    print(f"📝 Atualizando linha {row_number} | coluna 'Mensagem' (índice {message_col}) 📨 com a resposta: «{reply_message}»")


    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    sheet.update_cell(row_number, message_col, reply_message)
    sheet.update_cell(row_number, message_time_col, now)

    print(
        f"Resposta '{reply_message}' registrada para {phone_number} na linha {row_number}.")


def listar_telefones_e_status():
    client = authenticate_google()
    sheet = client.open(SHEET_NAME).worksheet(SHEET_LOG_PAGE)

    data = sheet.get_all_records()

    print("Lista de telefones e status na planilha:")
    for idx, row in enumerate(data, start=2):
        telefone = str(row.get('Telefone', '')).strip()
        status = str(row.get('Status', '')).strip()
        print(f"Linha {idx}: Telefone='{telefone}' | Status='{status}'")

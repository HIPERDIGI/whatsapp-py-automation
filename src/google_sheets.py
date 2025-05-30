import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

ZAPI_BASE_URL = os.getenv('ZAPI_BASE_URL')
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')
SHEET_NAME = os.getenv('SHEET_NAME')
SHEET_PAGE = os.getenv('SHEET_PAGE')
SHEET_LOG_PAGE = os.getenv('SHEET_LOG_PAGE')


SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']


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
    sheet = client.open(SHEET_NAME).worksheet(SHEET_PAGE)

    # Ler o cabeçalho (linha 1 de A até Z)
    header = sheet.range('A1:Z1')
    headers = [cell.value.strip().lower()
               for cell in header if cell.value.strip() != '']

    try:
        col_index = next(i for i, h in enumerate(
            headers) if 'telefone' in h) + 1
    except StopIteration:
        raise Exception(
            'Coluna com cabeçalho contendo "Telefone" não encontrada.')

    # Buscar todos os dados da coluna
    phone_numbers = sheet.col_values(col_index)
    phone_numbers = phone_numbers[1:]  # Ignorar cabeçalho

    # Limpar espaços e manter apenas números válidos
    return [p.strip() for p in phone_numbers if p.strip() and p.strip().isdigit()]

def log_sent_message(phone_number: str, status: str, sheet_name: str, sheet_page: str):
    client = authenticate_google()
    sheet = client.open(sheet_name).worksheet(sheet_page)

    # Obter o cabeçalho (primeira linha)
    header_row = sheet.row_values(1)

    # Mapear o índice de cada coluna
    try:
        phone_col = header_row.index('Telefone') + 1
        status_col = header_row.index('Status') + 1
        datetime_col = header_row.index('Data/Hora de Envio') + 1
    except ValueError as e:
        raise Exception(f"Erro: Cabeçalho não encontrado ou incorreto - {e}")

    now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    # Descobrir a próxima linha vazia
    next_row = len(sheet.col_values(1)) + 1

    # Inserir os dados nas colunas certas
    sheet.update_cell(next_row, phone_col, phone_number)
    sheet.update_cell(next_row, status_col, status)
    sheet.update_cell(next_row, datetime_col, now)

import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os


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
    sheet = client.open('teste').worksheet('Página1')

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

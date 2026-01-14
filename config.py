import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify', 
    'https://www.googleapis.com/auth/spreadsheets'  
]


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
TOKEN_FILE = os.path.join(BASE_DIR, 'credentials', 'token.json')
STATE_FILE = os.path.join(BASE_DIR, 'processed_emails.json')


SPREADSHEET_ID = '1C_wE3O-84O-MooxgN6zAUmTuyZJ5cR_jW1Yq_o8GMyw' 
RANGE_NAME = 'Sheet1!A1'
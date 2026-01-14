import os
import sys
import json
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.gmail_service import get_gmail_service, fetch_unread_emails, get_email_details, mark_as_read
from src.sheets_service import get_sheets_service, append_to_sheet
from src.email_parser import parse_email

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def authenticate():
    """Handles OAuth 2.0 Flow."""
    creds = None

    if os.path.exists(config.TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(config.TOKEN_FILE, config.SCOPES)
    
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(config.CREDENTIALS_FILE):
                logging.error("credentials.json not found in credentials/ folder.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(config.CREDENTIALS_FILE, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        
        with open(config.TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
            
    return creds

def load_processed_ids():
    """State persistence: Loads list of already processed email IDs."""
    if os.path.exists(config.STATE_FILE):
        with open(config.STATE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_processed_ids(processed_ids):
    """State persistence: Saves list of processed IDs."""
    with open(config.STATE_FILE, 'w') as f:
        json.dump(processed_ids, f)

def main():
    logging.info("Starting Email Automation...")
    
    
    creds = authenticate()
    if not creds:
        return

    gmail_service = get_gmail_service(creds)
    sheets_service = get_sheets_service(creds)
    
    
    processed_ids = load_processed_ids()
    
    
    messages = fetch_unread_emails(gmail_service)
    logging.info(f"Found {len(messages)} unread emails.")

    if not messages:
        logging.info("No new emails to process.")
        return

    new_rows = []
    processed_in_this_run = []

    for msg in messages:
        msg_id = msg['id']
        
        
        if msg_id in processed_ids:
            continue

        
        full_msg = get_email_details(gmail_service, msg_id)
        email_data = parse_email(full_msg)
        
        
        row = [
            email_data['from'],
            email_data['subject'],
            email_data['date'],
            email_data['content']
        ]
        new_rows.append(row)
        processed_in_this_run.append(msg_id)

    
    if new_rows:
        logging.info(f"Appending {len(new_rows)} rows to Sheets...")
        append_to_sheet(sheets_service, config.SPREADSHEET_ID, new_rows)
        
        
        for msg_id in processed_in_this_run:
            mark_as_read(gmail_service, msg_id)
            processed_ids.append(msg_id)
        
        save_processed_ids(processed_ids)
        logging.info("Success! Emails processed and marked as read.")
    else:
        logging.info("No valid new emails found (or all were duplicates).")

if __name__ == '__main__':
    main()
from googleapiclient.discovery import build

def get_gmail_service(creds):
    return build('gmail', 'v1', credentials=creds)

def fetch_unread_emails(service, max_results=10):
    """Fetches a list of unread email messages (IDs and Threads only)."""
    
    results = service.users().messages().list(userId='me', q='is:unread label:INBOX', maxResults=max_results).execute()
    messages = results.get('messages', [])
    return messages

def get_email_details(service, msg_id):
    """Fetches the full payload for a specific message ID."""
    return service.users().messages().get(userId='me', id=msg_id).execute()

def mark_as_read(service, msg_id):
    """Removes the 'UNREAD' label from a specific email."""
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
import base64

def clean_text(text, limit=4000):
    """
    Removes extra whitespace and truncates text to avoid Google Sheets 50k char limit.
    Default limit set to 4000 chars for readability.
    """
    if text:
        # Clean whitespace
        cleaned = " ".join(text.split())
        # Truncate to avoid 400 error
        if len(cleaned) > limit:
            return cleaned[:limit] + "... (TRUNCATED)"
        return cleaned
    return ""

def parse_email(message):
    """
    Parses a Gmail message object to extract required fields:
    From, Subject, Date, and Body (Content).
    """
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    
    email_data = {
        "id": message['id'],
        "from": "",
        "subject": "(No Subject)",
        "date": "",
        "content": ""
    }

    # 1. Extract Headers (From, Subject, Date)
    for header in headers:
        name = header['name'].lower()
        if name == 'from':
            email_data['from'] = header['value']
        elif name == 'subject':
            email_data['subject'] = header['value']
        elif name == 'date':
            email_data['date'] = header['value']

    # 2. Extract Body (Content)
    try:
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        email_data['content'] = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
            
            # If no plain text found, try main body or HTML part (fallback)
            if not email_data['content'] and 'body' in payload:
                 data = payload['body'].get('data')
                 if data:
                    email_data['content'] = base64.urlsafe_b64decode(data).decode('utf-8')

        elif 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            email_data['content'] = base64.urlsafe_b64decode(data).decode('utf-8')
            
    except Exception as e:
        email_data['content'] = f"(Error decoding email body: {str(e)})"

    # 3. Clean and Truncate
    email_data['content'] = clean_text(email_data['content'])
    
    return email_data
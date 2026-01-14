from googleapiclient.discovery import build

def get_sheets_service(creds):
    return build('sheets', 'v4', credentials=creds)

def append_to_sheet(service, spreadsheet_id, values):
    """
    Appends a list of rows to the spreadsheet.
    values: list of lists e.g. [['email', 'sub', 'date', 'body']]
    """
    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    return result
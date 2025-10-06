import gspread
from google.oauth2.service_account import Credentials
from flask import current_app

class GoogleSheetsService:
    def __init__(self):
        self.client = None
        self.spreadsheet = None
        self._connect()

    def _connect(self):
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds_path = current_app.config.get('GOOGLE_CREDENTIALS_PATH')
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        self.client = gspread.authorize(creds)
        sheet_id = current_app.config.get('GOOGLE_SHEET_ID')
        self.spreadsheet = self.client.open_by_key(sheet_id)

    def get_worksheet(self, name):
        try:
            return self.spreadsheet.worksheet(name)
        except Exception:
            return self.spreadsheet.add_worksheet(title=name, rows=1000, cols=20)

    def get_all_records(self, name):
        ws = self.get_worksheet(name)
        return ws.get_all_records()

    def add_record(self, name, data):
        ws = self.get_worksheet(name)
        headers = ws.row_values(1)
        if not headers:
            headers = list(data.keys())
            ws.append_row(headers)
        values = [data.get(h, '') for h in headers]
        ws.append_row(values)
        return True
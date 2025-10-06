#!/usr/bin/env python3
import os
from dotenv import load_dotenv
load_dotenv()
print('Migrating from Google Sheets to Postgres...')
# This script expects GOOGLE_MODE and POSTGRES_URL set.
# It uses gspread to read sheets and psycopg2 to insert rows.
# For safety, it's a minimal scaffold - adapt to your schemas before running in production.
try:
    import gspread
    from google.oauth2.service_account import Credentials
    from lib.database import db
    scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(os.getenv('GOOGLE_CREDENTIALS_PATH'), scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(os.getenv('GOOGLE_SHEET_ID'))
    # Example: migrate parking_spaces
    ws = sheet.worksheet('parking_spaces')
    rows = ws.get_all_records()
    for r in rows:
        try:
            db.execute('INSERT INTO parking_spaces (space_number, is_occupied, is_reserved, space_type, status, floor, zone) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (space_number) DO NOTHING',
                       (r.get('space_number'), r.get('is_occupied') in ('True', True), r.get('is_reserved') in ('True', True), r.get('space_type'), r.get('status'), r.get('floor'), r.get('zone')))
        except Exception as e:
            print('Error inserting', r, e)
    print('Migration finished (partial demo).')
except Exception as e:
    print('Migration failed:', e)
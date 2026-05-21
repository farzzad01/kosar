import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nobatdehi.settings')
django.setup()

from appointments.google_sheets_service import GoogleSheetsService

try:
    print("Testing Google Sheets connection...")
    service = GoogleSheetsService()
    print("✅ Connected successfully!")
    print(f"Spreadsheet: {service.spreadsheet.title}")
    print(f"Sheet: {service.sheet.title}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

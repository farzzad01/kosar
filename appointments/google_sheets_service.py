import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os

class GoogleSheetsService:
    def __init__(self):
        """Initialize Google Sheets API"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        creds_path = os.path.join(settings.BASE_DIR, 'decent-destiny-466517-k1-18a0c65a31ea.json')
        
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Credentials file not found at {creds_path}")
        
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        self.client = gspread.authorize(self.creds)
        
        # Open by spreadsheet ID
        SPREADSHEET_ID = '1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlRSXC79iz-8dc'
        self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
        self.sheet = self.spreadsheet.sheet1
        
        # Setup headers if needed
        if not self.sheet.row_values(1):
            self.setup_headers()
    
    def setup_headers(self):
        """Setup column headers"""
        headers = [
            'ID',
            'الاسم',
            'الاسم بحسب الجواز',
            'المقطع',
            'التخصص',
            'نوع الجامعة',
            'جامعة البكالوريوس',
            'جامعة الماجستير',
            'رقم الهاتف',
            'ملف جواز السفر',
            'ملف شهادة البكالوريوس',
            'ملف شهادة الماجستير',
            'ملف كشف درجات البكالوريوس',
            'ملف كشف درجات الماجستير',
            'ملف الاستمارة المعبأة',
            'تاريخ التسجيل'
        ]
        self.sheet.append_row(headers)
        
        # Format header
        try:
            self.sheet.format('A1:P1', {
                'backgroundColor': {'red': 0.83, 'green': 0.69, 'blue': 0.22},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                'horizontalAlignment': 'CENTER'
            })
        except:
            pass  # Formatting is optional
    
    def add_row(self, data):
        """Add new row"""
        self.sheet.append_row(data)
        return self.sheet.row_count

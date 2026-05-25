import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
import json

class GoogleSheetsService:
    def __init__(self):
        """Initialize Google Sheets API"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        # Try to get credentials from environment variable first (for Vercel)
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        
        if creds_json:
            # Parse JSON from environment variable
            try:
                creds_dict = json.loads(creds_json)
                self.creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
                print("[DEBUG] Using credentials from environment variable")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in GOOGLE_CREDENTIALS_JSON: {str(e)}")
        else:
            # Fallback to file (for local development)
            creds_path = os.path.join(settings.BASE_DIR, 'decent-destiny-466517-k1-18a0c65a31ea.json')
            
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"Credentials not found. Please set GOOGLE_CREDENTIALS_JSON environment variable "
                    f"or place credentials file at {creds_path}"
                )
            
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
            print("[DEBUG] Using credentials from file")
        
        self.client = gspread.authorize(self.creds)
        
        # Open by spreadsheet ID
        SPREADSHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlRSXC79iz-8dc')
        self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
        self.sheet = self.spreadsheet.sheet1
        
        # Setup headers if needed
        if not self.sheet.row_values(1):
            self.setup_headers()
    
    def setup_headers(self):
        """Setup column headers"""
        headers = [
            'ID',
            'الاسم الكامل',
            'الديانة',
            'رقم الهاتف',
            'البريد الإلكتروني',
            'العنوان في العراق',
            'الوظيفة',
            'الحالة الاجتماعية',
            'عدد الأطفال',
            'نوع الجامعة',
            'المقطع',
            'التخصص',
            'الجامعة السابقة',
            'معدل البكالوريوس',
            'معدل الماجستير',
            'ملف جواز السفر',
            'ملف كشف درجات البكالوريوس',
            'ملف كشف درجات الماجستير',
            'ملف السيرة الذاتية',
            'تاريخ التسجيل'
        ]
        self.sheet.append_row(headers)
        
        # Format header
        try:
            self.sheet.format('A1:T1', {
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

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import os
from datetime import datetime

class GoogleSheetsService:
    def __init__(self):
        """Initialize Google Sheets API"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        # Path to credentials file
        creds_path = os.path.join(settings.BASE_DIR, 'decent-destiny-466517-k1-18a0c65a31ea.json')
        
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Credentials file not found at {creds_path}")
        
        # Authenticate
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        self.client = gspread.authorize(self.creds)
        
        # Open spreadsheet by key or create new one
        try:
            # Try to open existing spreadsheet
            self.spreadsheet = self.client.open('Student_Registrations')
        except gspread.SpreadsheetNotFound:
            # Create new spreadsheet
            self.spreadsheet = self.client.create('Student_Registrations')
            # Share with service account email
            self.spreadsheet.share('vercel-sheets-connector@decent-destiny-466517-k1.iam.gserviceaccount.com', 
                                  perm_type='user', role='writer')
        
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
            'رابط جواز السفر',
            'رابط شهادة البكالوريوس',
            'رابط شهادة الماجستير',
            'رابط كشف درجات البكالوريوس',
            'رابط كشف درجات الماجستير',
            'رابط الاستمارة المعبأة',
            'تاريخ التسجيل'
        ]
        self.sheet.append_row(headers)
        
        # Format header row
        self.sheet.format('A1:P1', {
            'backgroundColor': {'red': 0.83, 'green': 0.69, 'blue': 0.22},
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
            'horizontalAlignment': 'CENTER'
        })
    
    def add_row(self, data):
        """Add new row to sheet"""
        self.sheet.append_row(data)
        return self.sheet.row_count
    
    def upload_to_drive(self, file_obj, filename, student_name=''):
        """
        Upload file to Google Drive and return shareable link
        For now, returns a placeholder. You can implement full Drive upload later.
        """
        # Placeholder - in production, implement full Drive API upload
        return f"https://drive.google.com/file/{filename}"

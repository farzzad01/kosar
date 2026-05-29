import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from django.conf import settings
import os
import json
import tempfile

class GoogleSheetsService:
    def __init__(self):
        """Initialize Google Sheets API and Google Drive"""
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
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
        
        # Initialize Sheets
        self.client = gspread.authorize(self.creds)
        
        # Open by spreadsheet ID
        SPREADSHEET_ID = os.environ.get('GOOGLE_SHEET_ID', '1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlRSXC79iz-8dc')
        self.spreadsheet = self.client.open_by_key(SPREADSHEET_ID)
        self.sheet = self.spreadsheet.sheet1
        
        # Initialize Drive
        self.drive = self._init_drive()
        
        # Get or create folder for uploads
        self.folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '')
        
        # Setup headers and formatting if needed
        if not self.sheet.row_values(1):
            self.setup_headers()
        else:
            # Apply formatting to existing sheet
            self.apply_rtl_formatting()
    
    def _init_drive(self):
        """Initialize Google Drive"""
        try:
            gauth = GoogleAuth()
            gauth.credentials = self.creds
            return GoogleDrive(gauth)
        except Exception as e:
            print(f"[WARNING] Could not initialize Google Drive: {str(e)}")
            return None
    
    def upload_to_drive(self, file_obj, filename, registration_id):
        """Upload file to Google Drive and return shareable link"""
        if not self.drive:
            print("[WARNING] Google Drive not initialized, skipping upload")
            return filename
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp_file:
                for chunk in file_obj.chunks():
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name
            
            # Upload to Drive
            file_metadata = {
                'title': f"{registration_id}_{filename}",
            }
            
            if self.folder_id:
                file_metadata['parents'] = [{'id': self.folder_id}]
            
            drive_file = self.drive.CreateFile(file_metadata)
            drive_file.SetContentFile(tmp_path)
            drive_file.Upload()
            
            # Make file publicly accessible
            drive_file.InsertPermission({
                'type': 'anyone',
                'value': 'anyone',
                'role': 'reader'
            })
            
            # Get shareable link
            file_url = drive_file['alternateLink']
            
            # Clean up temp file
            os.unlink(tmp_path)
            
            print(f"[DEBUG] Uploaded {filename} to Drive: {file_url}")
            return file_url
            
        except Exception as e:
            print(f"[ERROR] Failed to upload {filename} to Drive: {str(e)}")
            return filename
    
    def setup_headers(self):
        """Setup column headers with RTL and formatting"""
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
            'الجامعة السابقة (البكالوريوس)',
            'الجامعة السابقة (الماجستير)',
            'معدل البكالوريوس',
            'معدل الماجستير',
            'ملف جواز السفر',
            'ملف صورة الشخص',
            'ملف كشف درجات البكالوريوس',
            'ملف كشف درجات الماجستير',
            'ملف وثيقة الماجستير',
            'تاريخ التسجيل'
        ]
        self.sheet.append_row(headers)
        
        # Apply formatting
        self.apply_rtl_formatting()
    
    def apply_rtl_formatting(self):
        """Apply RTL direction and formatting to the sheet"""
        try:
            # Format header row (bold, colored background, larger font, centered)
            self.sheet.format('A1:V1', {
                'backgroundColor': {'red': 0.83, 'green': 0.69, 'blue': 0.22},
                'textFormat': {
                    'bold': True,
                    'fontSize': 14,
                    'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}
                },
                'horizontalAlignment': 'CENTER',
                'verticalAlignment': 'MIDDLE'
            })
            
            # Format all data cells (RTL, larger font)
            self.sheet.format('A2:V1000', {
                'textFormat': {
                    'fontSize': 12
                },
                'horizontalAlignment': 'RIGHT',
                'verticalAlignment': 'MIDDLE',
                'wrapStrategy': 'WRAP'
            })
            
            # Set column widths
            requests = [
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': self.sheet.id,
                            'dimension': 'COLUMNS',
                            'startIndex': 0,
                            'endIndex': 22
                        },
                        'properties': {
                            'pixelSize': 150
                        },
                        'fields': 'pixelSize'
                    }
                },
                {
                    'updateDimensionProperties': {
                        'range': {
                            'sheetId': self.sheet.id,
                            'dimension': 'ROWS',
                            'startIndex': 0,
                            'endIndex': 1
                        },
                        'properties': {
                            'pixelSize': 40
                        },
                        'fields': 'pixelSize'
                    }
                }
            ]
            
            self.spreadsheet.batch_update({'requests': requests})
            
            print("[DEBUG] Applied RTL formatting to sheet")
            
        except Exception as e:
            print(f"[WARNING] Could not apply formatting: {str(e)}")
    
    def add_row(self, data, files=None):
        """Add new row with optional file uploads to Drive"""
        # If files provided, upload them and replace filenames with Drive links
        if files:
            registration_id = data[0]  # First column is ID
            
            # File columns: 16-20 (passport, personal_photo, transcript, master_transcript, master_certificate)
            file_columns = [16, 17, 18, 19, 20]
            file_keys = ['passport', 'personal_photo', 'transcript', 'master_transcript', 'master_certificate']
            
            for idx, key in enumerate(file_keys):
                if key in files and files[key]:
                    file_obj = files[key]
                    drive_link = self.upload_to_drive(file_obj, file_obj.name, registration_id)
                    data[file_columns[idx]] = drive_link
        
        self.sheet.append_row(data)
        return self.sheet.row_count

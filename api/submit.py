import json
import os
from http.server import BaseHTTPRequestHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # خواندن داده‌های فرم
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # اتصال به Google Sheets
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            
            # خواندن credentials از environment variable
            creds_json = os.environ.get('GOOGLE_CREDENTIALS')
            if not creds_json:
                raise Exception('GOOGLE_CREDENTIALS not found')
            
            creds_dict = json.loads(creds_json)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            
            # باز کردن Google Sheet
            sheet_id = os.environ.get('GOOGLE_SHEET_ID')
            if not sheet_id:
                raise Exception('GOOGLE_SHEET_ID not found')
            
            sheet = client.open_by_key(sheet_id).sheet1
            
            # آماده‌سازی داده برای ذخیره
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                data.get('name', ''),
                data.get('phone', ''),
                data.get('degree', ''),
                data.get('appointment_date', ''),
                data.get('appointment_time', ''),
                data.get('reason', ''),
                data.get('duration', '')
            ]
            
            # اضافه کردن به Sheet
            sheet.append_row(row)
            
            # پاسخ موفقیت
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'تم حجز موعدك بنجاح! في انتظار حضورك'
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

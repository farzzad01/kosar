import json
import os
from http.server import BaseHTTPRequestHandler
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def get_sheet(self):
        """تابع کمکی برای اتصال به گوگل شیت"""
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        creds_json = os.environ.get('GOOGLE_CREDENTIALS')
        if not creds_json:
            raise Exception('GOOGLE_CREDENTIALS not found')
            
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        sheet_id = os.environ.get('GOOGLE_SHEET_ID')
        if not sheet_id:
            raise Exception('GOOGLE_SHEET_ID not found')
            
        return client.open_by_key(sheet_id).sheet1

    def do_GET(self):
        """خواندن تعداد رزروهای امروز برای نمایش در اسلات‌های زمانی"""
        try:
            sheet = self.get_sheet()
            records = sheet.get_all_records()
            today = datetime.now().strftime('%Y-%m-%d')
            
            # شمارش رزروها برای هر ساعت در تاریخ امروز
            stats = {}
            for row in records:
                # فرض بر این است که نام ستون‌ها در شیت شما دقیقا مطابق فیلدهای ارسالی است
                if str(row.get('appointment_date')) == today:
                    time_val = str(row.get('appointment_time', ''))
                    if time_val:
                        # تبدیل زمان (مثلا 19:20) به ساعت رند (19:00) برای دسته‌بندی
                        hour_key = time_val.split(':')[0] + ":00"
                        stats[hour_key] = stats.get(hour_key, 0) + 1
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

    def do_POST(self):
        """ثبت رزرو جدید در گوگل شیت"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            sheet = self.get_sheet()
            
            # آماده‌سازی ردیف برای درج در شیت
            row = [
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # زمان ثبت سیستم
                data.get('name', ''),
                data.get('phone', ''),
                data.get('degree', ''),
                data.get('appointment_date', ''),
                data.get('appointment_time', ''),
                data.get('reason', ''),
                data.get('duration', '')
            ]
            
            sheet.append_row(row)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'message': 'تم حجز موعدك بنجاح!'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))

    def do_OPTIONS(self):
        """مدیریت درخواست‌های پیش‌پرواز مرورگر"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
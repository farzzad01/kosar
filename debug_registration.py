#!/usr/bin/env python
"""
دیباگر فرم ثبت‌نام - تشخیص مشکلات احتمالی
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nobatdehi.settings')
django.setup()

from django.conf import settings
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def check_environment():
    """بررسی متغیرهای محیطی"""
    print("=" * 60)
    print("1. بررسی متغیرهای محیطی")
    print("=" * 60)
    
    env_vars = [
        'GOOGLE_SHEETS_CREDENTIALS',
        'GOOGLE_SHEET_ID',
        'DEBUG',
        'SECRET_KEY'
    ]
    
    for var in env_vars:
        value = os.environ.get(var, 'NOT SET')
        if var == 'SECRET_KEY' and value != 'NOT SET':
            value = '***HIDDEN***'
        print(f"  {var}: {value}")
    print()

def check_credentials_file():
    """بررسی فایل اعتبارسنجی Google"""
    print("=" * 60)
    print("2. بررسی فایل اعتبارسنجی Google")
    print("=" * 60)
    
    creds_path = os.path.join(settings.BASE_DIR, 'decent-destiny-466517-k1-18a0c65a31ea.json')
    
    if os.path.exists(creds_path):
        print(f"  ✓ فایل پیدا شد: {creds_path}")
        file_size = os.path.getsize(creds_path)
        print(f"  ✓ حجم فایل: {file_size} بایت")
        
        try:
            import json
            with open(creds_path, 'r') as f:
                creds_data = json.load(f)
                print(f"  ✓ فایل JSON معتبر است")
                print(f"  ✓ نوع: {creds_data.get('type', 'نامشخص')}")
                print(f"  ✓ Project ID: {creds_data.get('project_id', 'نامشخص')}")
                print(f"  ✓ Client Email: {creds_data.get('client_email', 'نامشخص')}")
        except Exception as e:
            print(f"  ✗ خطا در خواندن فایل: {str(e)}")
    else:
        print(f"  ✗ فایل پیدا نشد: {creds_path}")
    print()

def check_google_sheets_connection():
    """بررسی اتصال به Google Sheets"""
    print("=" * 60)
    print("3. بررسی اتصال به Google Sheets")
    print("=" * 60)
    
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        
        creds_path = os.path.join(settings.BASE_DIR, 'decent-destiny-466517-k1-18a0c65a31ea.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        
        print("  ✓ احراز هویت موفق")
        
        SPREADSHEET_ID = '1Jn2UaFzUE_4BOveyZ9Ryjz40tu6_RqlRSXC79iz-8dc'
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        
        print(f"  ✓ اتصال به Spreadsheet موفق")
        print(f"  ✓ عنوان: {spreadsheet.title}")
        
        sheet = spreadsheet.sheet1
        print(f"  ✓ دسترسی به Sheet1 موفق")
        print(f"  ✓ تعداد ردیف‌ها: {sheet.row_count}")
        print(f"  ✓ تعداد ستون‌ها: {sheet.col_count}")
        
        # Test write
        test_data = ['TEST', 'تست', '123', 'test@test.com']
        print("\n  در حال تست نوشتن...")
        sheet.append_row(test_data)
        print("  ✓ نوشتن موفق")
        
        # Delete test row
        last_row = sheet.row_count
        sheet.delete_rows(last_row)
        print("  ✓ حذف ردیف تست موفق")
        
    except FileNotFoundError as e:
        print(f"  ✗ فایل اعتبارسنجی پیدا نشد: {str(e)}")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"  ✗ Spreadsheet پیدا نشد - ID اشتباه است یا دسترسی وجود ندارد")
    except gspread.exceptions.APIError as e:
        print(f"  ✗ خطای API: {str(e)}")
    except Exception as e:
        print(f"  ✗ خطا: {str(e)}")
        import traceback
        print(traceback.format_exc())
    print()

def check_static_files():
    """بررسی فایل‌های استاتیک (لوگو)"""
    print("=" * 60)
    print("4. بررسی فایل‌های استاتیک (لوگو)")
    print("=" * 60)
    
    logo_files = [
        'static/logoo.png',
        'static/logokosar.jpg',
        'static/logooo.png',
        'assets/logoo.png',
        'assets/logogg/logokosar.jpg'
    ]
    
    for logo_path in logo_files:
        full_path = os.path.join(settings.BASE_DIR, logo_path)
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            print(f"  ✓ {logo_path} - {file_size} بایت")
        else:
            print(f"  ✗ {logo_path} - پیدا نشد")
    print()

def check_database():
    """بررسی دیتابیس"""
    print("=" * 60)
    print("5. بررسی دیتابیس")
    print("=" * 60)
    
    try:
        from appointments.models import StudentRegistration
        
        count = StudentRegistration.objects.count()
        print(f"  ✓ تعداد ثبت‌نام‌ها: {count}")
        
        if count > 0:
            latest = StudentRegistration.objects.latest('created_at')
            print(f"  ✓ آخرین ثبت‌نام: {latest.first_name} {latest.last_name}")
            print(f"  ✓ تاریخ: {latest.created_at}")
    except Exception as e:
        print(f"  ✗ خطا: {str(e)}")
    print()

def check_form_validation():
    """بررسی اعتبارسنجی فرم"""
    print("=" * 60)
    print("6. نکات مهم فرم")
    print("=" * 60)
    
    print("  • فیلدهای اجباری:")
    print("    - نام، نام خانوادگی، دین، تلفن، ایمیل")
    print("    - آدرس، شغل، وضعیت تاهل")
    print("    - نوع دانشگاه، مقطع، رشته")
    print("    - دانشگاه قبلی، معدل کارشناسی")
    print("    - فایل‌های: پاسپورت، ریز نمرات، CV")
    print()
    print("  • فیلدهای شرطی:")
    print("    - تعداد فرزندان (اگر متاهل)")
    print("    - معدل کارشناسی ارشد (اگر دکترا)")
    print("    - ریز نمرات کارشناسی ارشد (اگر دکترا)")
    print()
    print("  • محدودیت‌های فایل:")
    print("    - فرمت‌های مجاز: تصویر (jpg, png) یا PDF")
    print("    - حداکثر حجم: بررسی شود در settings.py")
    print()

def check_network_issues():
    """بررسی مشکلات شبکه"""
    print("=" * 60)
    print("7. بررسی اتصال شبکه")
    print("=" * 60)
    
    import socket
    
    hosts = [
        ('sheets.googleapis.com', 443),
        ('www.googleapis.com', 443),
        ('accounts.google.com', 443)
    ]
    
    for host, port in hosts:
        try:
            socket.create_connection((host, port), timeout=5)
            print(f"  ✓ اتصال به {host}:{port} موفق")
        except Exception as e:
            print(f"  ✗ اتصال به {host}:{port} ناموفق: {str(e)}")
    print()

def main():
    """اجرای تمام تست‌ها"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "دیباگر فرم ثبت‌نام" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    check_environment()
    check_credentials_file()
    check_static_files()
    check_database()
    check_google_sheets_connection()
    check_network_issues()
    check_form_validation()
    
    print("=" * 60)
    print("تست‌ها تمام شد")
    print("=" * 60)
    print()
    
    print("راهنمای رفع مشکلات:")
    print("-" * 60)
    print("1. اگر خطای 'حدث خطأ أثناء الإرسال' می‌بینید:")
    print("   - بررسی کنید اتصال اینترنت فعال است")
    print("   - بررسی کنید فایل اعتبارسنجی Google موجود است")
    print("   - بررسی کنید Spreadsheet ID صحیح است")
    print()
    print("2. اگر لوگو نمایش داده نمی‌شود:")
    print("   - بررسی کنید فایل لوگو در مسیر static/logoo.png وجود دارد")
    print("   - دستور collectstatic را اجرا کنید")
    print("   - حجم فایل را کاهش دهید (کمتر از 500KB)")
    print()
    print("3. اگر فایل‌ها آپلود نمی‌شوند:")
    print("   - بررسی کنید FILE_UPLOAD_MAX_MEMORY_SIZE در settings")
    print("   - بررسی کنید MEDIA_ROOT و MEDIA_URL تنظیم شده‌اند")
    print("   - حجم فایل را کاهش دهید")
    print()

if __name__ == '__main__':
    main()

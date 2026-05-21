import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nobatdehi.settings')
django.setup()

from appointments.google_sheets_service import GoogleSheetsService
from datetime import datetime

try:
    print("Testing data submission to Google Sheets...")
    service = GoogleSheetsService()
    
    # Test data
    test_data = [
        '1',
        'أحمد محمد',
        'Ahmed Mohammed',
        'ماجستير',
        'علوم الحاسوب',
        'نفقة خاصة',
        'جامعة بغداد',
        '',
        '+964 770 123 4567',
        'passport.pdf',
        'bachelor.pdf',
        '',
        'transcript.pdf',
        '',
        'form.pdf',
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ]
    
    row_number = service.add_row(test_data)
    print(f"✅ Data added successfully at row {row_number}!")
    print("Check your Google Sheet now!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

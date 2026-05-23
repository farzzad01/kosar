#!/usr/bin/env python
"""Test Google Sheets connection"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nobatdehi.settings')
django.setup()

from appointments.google_sheets_service import GoogleSheetsService
from datetime import datetime

def test_connection():
    """Test Google Sheets connection and data writing"""
    try:
        print("🔄 Connecting to Google Sheets...")
        sheets_service = GoogleSheetsService()
        print("✅ Connected successfully!")
        
        print("\n📝 Testing data write...")
        test_data = [
            'TEST-001',
            'علی احمدی',
            'Ali Ahmadi',
            '+964 770 123 4567',
            'بغداد',
            'مهندس',
            'متأهل',
            '2',
            'نفقة خاصة',
            'ماجستير',
            'علوم الحاسوب',
            '85.5',
            '',
            'passport_test.pdf',
            'transcript_test.pdf',
            'form_test.pdf',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
        
        row_number = sheets_service.add_row(test_data)
        print(f"✅ Test data added successfully at row {row_number}")
        print("\n🎉 All tests passed!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)

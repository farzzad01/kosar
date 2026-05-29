"""
Test Google Drive connection
Run this locally to test if Drive upload works
"""

import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

def test_drive():
    print("=" * 50)
    print("Testing Google Drive Connection")
    print("=" * 50)
    
    # Load credentials
    creds_path = 'decent-destiny-466517-k1-18a0c65a31ea.json'
    
    if not os.path.exists(creds_path):
        print("❌ Credentials file not found!")
        return False
    
    print("✅ Credentials file found")
    
    try:
        # Initialize credentials
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        print("✅ Credentials loaded")
        
        # Initialize Drive
        gauth = GoogleAuth()
        gauth.credentials = creds
        drive = GoogleDrive(gauth)
        print("✅ Google Drive initialized")
        
        # Try to create a test file
        test_file = drive.CreateFile({'title': 'test_connection.txt'})
        test_file.SetContentString('This is a test file')
        test_file.Upload()
        print("✅ Test file uploaded")
        
        # Make it public
        test_file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        print("✅ File made public")
        
        # Get link
        file_url = test_file['alternateLink']
        print(f"✅ File URL: {file_url}")
        
        # Delete test file
        test_file.Delete()
        print("✅ Test file deleted")
        
        print("\n" + "=" * 50)
        print("🎉 SUCCESS! Google Drive is working!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        print("\n" + "=" * 50)
        print("❌ FAILED! Google Drive is NOT working")
        print("=" * 50)
        return False

if __name__ == '__main__':
    test_drive()

"""
Test Google Drive upload with shared folder
"""

import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

def test_drive_with_folder():
    print("=" * 60)
    print("Testing Google Drive Upload with Shared Folder")
    print("=" * 60)
    
    # Configuration
    creds_path = 'decent-destiny-466517-k1-18a0c65a31ea.json'
    folder_id = '1gACUvgy6Qm29TiRKfOx73DZGzwgru7hD'
    
    if not os.path.exists(creds_path):
        print("❌ Credentials file not found!")
        return False
    
    print("✅ Credentials file found")
    print(f"✅ Folder ID: {folder_id}")
    
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
        
        # Try to create a test file IN THE SHARED FOLDER
        print(f"\n📁 Uploading to shared folder: {folder_id}")
        
        test_file = drive.CreateFile({
            'title': 'test_upload.txt',
            'parents': [{'id': folder_id}]  # Upload to shared folder
        })
        test_file.SetContentString('This is a test file uploaded to shared folder!')
        test_file.Upload()
        print("✅ Test file uploaded to shared folder")
        
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
        
        # Don't delete - keep it for verification
        print("\n⚠️  File NOT deleted - check your Drive folder to verify!")
        print(f"   Go to: https://drive.google.com/drive/folders/{folder_id}")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Google Drive upload is working!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("1. Check your Google Drive folder to see the test file")
        print("2. Add GOOGLE_DRIVE_FOLDER_ID to Vercel Environment Variables")
        print(f"   Value: {folder_id}")
        print("3. Redeploy your Vercel project")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        print("\n" + "=" * 60)
        print("❌ FAILED! Check the error above")
        print("=" * 60)
        print("\n🔍 Common issues:")
        print("1. Did you share the folder with the service account email?")
        print("2. Did you give 'Editor' permission?")
        print("3. Is the folder ID correct?")
        return False

if __name__ == '__main__':
    test_drive_with_folder()

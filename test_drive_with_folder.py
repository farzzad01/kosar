"""
Test Google Drive upload with shared folder
"""

import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

def test_drive_with_folder():
    print("=" * 60)
    print("Testing Google Drive Upload with Shared Folder")
    print("=" * 60)
    
    # Load credentials
    creds_path = 'decent-destiny-466517-k1-18a0c65a31ea.json'
    
    if not os.path.exists(creds_path):
        print("❌ Credentials file not found!")
        return False
    
    print("✅ Credentials file found")
    
    # Get folder ID from environment or ask user
    folder_id = os.environ.get('GOOGLE_DRIVE_FOLDER_ID', '')
    
    if not folder_id:
        print("\n⚠️  GOOGLE_DRIVE_FOLDER_ID not set!")
        print("Please enter your Google Drive Folder ID:")
        print("(Get it from the folder URL: folders/YOUR_FOLDER_ID)")
        folder_id = input("Folder ID: ").strip()
    
    if not folder_id:
        print("❌ No folder ID provided!")
        return False
    
    print(f"✅ Using folder ID: {folder_id}")
    
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
        
        # Try to create a test file in the shared folder
        print(f"\n📤 Uploading test file to folder {folder_id}...")
        
        test_file = drive.CreateFile({
            'title': 'test_connection.txt',
            'parents': [{'id': folder_id}]  # Upload to shared folder
        })
        test_file.SetContentString('This is a test file from Service Account')
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
        
        # Ask if user wants to delete
        print("\n🗑️  Delete test file? (y/n): ", end='')
        delete = input().strip().lower()
        
        if delete == 'y':
            test_file.Delete()
            print("✅ Test file deleted")
        else:
            print("ℹ️  Test file kept in Drive")
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Google Drive upload is working!")
        print("=" * 60)
        print("\n📝 Next steps:")
        print("1. Add this to Vercel Environment Variables:")
        print(f"   GOOGLE_DRIVE_FOLDER_ID={folder_id}")
        print("2. Redeploy your project")
        print("3. Test file upload from the website")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        print(traceback.format_exc())
        print("\n" + "=" * 60)
        print("❌ FAILED! Check the error above")
        print("=" * 60)
        print("\n💡 Common issues:")
        print("1. Folder not shared with Service Account")
        print("2. Wrong folder ID")
        print("3. Service Account doesn't have Editor access")
        print("\n📖 See DRIVE_SETUP_GUIDE.md for detailed instructions")
        return False

if __name__ == '__main__':
    test_drive_with_folder()

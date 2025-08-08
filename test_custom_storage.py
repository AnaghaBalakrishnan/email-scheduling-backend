#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.core.files.base import ContentFile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.storage import ProfilePictureStorage

def test_custom_storage():
    """Test custom profile picture storage"""
    print("🧪 Testing custom profile picture storage...")
    
    # Create custom storage instance
    storage = ProfilePictureStorage()
    print(f"📦 Custom Storage class: {storage.__class__}")
    print(f"📦 Storage location: {storage.location}")
    
    # Test file content
    test_content = b"This is a custom storage test file"
    test_filename = "test_custom_storage.txt"
    
    try:
        # Upload test file
        print(f"📤 Uploading test file: {test_filename}")
        path = storage.save(test_filename, ContentFile(test_content))
        print(f"✅ File uploaded successfully to: {path}")
        
        # Check if file exists
        if storage.exists(path):
            print(f"✅ File exists in S3: {path}")
            
            # Get file URL
            url = storage.url(path)
            print(f"🔗 File URL: {url}")
            
            # Check if it's an S3 URL
            if 's3.amazonaws.com' in url or 'amazonaws.com' in url:
                print("✅ File is stored in S3!")
            else:
                print("❌ File is stored locally, not in S3")
            
            # Delete test file
            storage.delete(path)
            print(f"🗑️  Test file deleted")
            
            return True
        else:
            print(f"❌ File does not exist in S3: {path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during custom storage test: {str(e)}")
        return False

if __name__ == "__main__":
    test_custom_storage()

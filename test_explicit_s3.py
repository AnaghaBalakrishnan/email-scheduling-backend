#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.core.files.base import ContentFile
from storages.backends.s3boto3 import S3Boto3Storage

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def test_explicit_s3_storage():
    """Test explicit S3 storage"""
    print("🧪 Testing explicit S3 storage...")
    
    # Create S3 storage instance
    s3_storage = S3Boto3Storage()
    print(f"📦 S3 Storage class: {s3_storage.__class__}")
    print(f"📦 S3 Bucket: {s3_storage.bucket_name}")
    
    # Test file content
    test_content = b"This is an explicit S3 test file"
    test_filename = "profile_pics/explicit_test.txt"
    
    try:
        # Upload test file
        print(f"📤 Uploading test file: {test_filename}")
        path = s3_storage.save(test_filename, ContentFile(test_content))
        print(f"✅ File uploaded successfully to: {path}")
        
        # Check if file exists
        if s3_storage.exists(path):
            print(f"✅ File exists in S3: {path}")
            
            # Get file URL
            url = s3_storage.url(path)
            print(f"🔗 File URL: {url}")
            
            # Delete test file
            s3_storage.delete(path)
            print(f"🗑️  Test file deleted")
            
            return True
        else:
            print(f"❌ File does not exist in S3: {path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during explicit S3 test: {str(e)}")
        return False

if __name__ == "__main__":
    test_explicit_s3_storage()

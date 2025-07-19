#!/usr/bin/env python3
"""
Enhanced error monitoring for Cloudinary uploads
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eesa_backend.settings')
import django
django.setup()

from django.conf import settings
import logging


# Setup enhanced logging for Cloudinary issues
def setup_cloudinary_logging():
    """Setup detailed logging for Cloudinary operations"""
    
    # Create a specific logger for Cloudinary
    cloudinary_logger = logging.getLogger('cloudinary_debug')
    cloudinary_logger.setLevel(logging.DEBUG)
    
    # Create file handler for Cloudinary logs
    handler = logging.FileHandler('cloudinary_debug.log')
    handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    cloudinary_logger.addHandler(handler)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    cloudinary_logger.addHandler(console_handler)
    
    return cloudinary_logger


def monitor_cloudinary_uploads():
    """Monitor and log Cloudinary upload activities"""
    
    logger = setup_cloudinary_logging()
    
    print("🔍 Cloudinary Upload Monitor Started")
    print("📁 Debug logs will be written to: cloudinary_debug.log")
    print("📋 This will help identify 'unsupported format' errors")
    print("\nTo use this monitor:")
    print("1. Keep this script running")
    print("2. Try uploading files through your admin interface")
    print("3. Check the logs for detailed error information")
    print("4. Look for patterns in failed uploads")
    
    # Log current configuration
    logger.info("=== Cloudinary Configuration ===")
    logger.info(f"Storage Backend: {settings.STORAGES['default']['BACKEND']}")
    logger.info(f"Media URL: {settings.MEDIA_URL}")
    
    try:
        from decouple import config
        cloud_name = config('CLOUDINARY_CLOUD_NAME', default='not_set')
        logger.info(f"Cloud Name: {cloud_name}")
        
        # Test basic connectivity
        import cloudinary.api
        ping_result = cloudinary.api.ping()
        logger.info(f"API Ping: {ping_result}")
        
    except Exception as e:
        logger.error(f"Configuration check failed: {e}")
    
    logger.info("=== Monitor Ready ===")
    
    # Instructions for enabling Django logging
    print("\n💡 To get more detailed upload logs, add this to your Django admin view:")
    print("""
import logging
logger = logging.getLogger('cloudinary_debug')

# In your upload handling code:
try:
    # Upload code here
    logger.info(f"Upload successful: {file_name}")
except Exception as e:
    logger.error(f"Upload failed: {file_name} - Error: {e}")
    """)
    
    print("\n🚀 Ready to monitor uploads. Try uploading a file now...")
    
    # Keep the script running to monitor
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped")
        logger.info("=== Monitor Stopped ===")


if __name__ == "__main__":
    monitor_cloudinary_uploads()

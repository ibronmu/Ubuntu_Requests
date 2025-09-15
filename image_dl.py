#!/usr/bin/env python3
"""
Image Fetcher - A utility to download images from URLs
Implements Ubuntu principles: Community, Respect, Sharing, Practicality
"""

import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path
import mimetypes
from datetime import datetime

def create_directory(directory_name="Fetched_Images"):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(directory_name, exist_ok=True)
        print(f"✓ Directory '{directory_name}' is ready")
        return directory_name
    except PermissionError:
        print("✗ Permission denied: Cannot create directory")
        return None
    except Exception as e:
        print(f"✗ Error creating directory: {e}")
        return None

def extract_filename_from_url(url):
    """Extract filename from URL or generate one if not available"""
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    
    # Try to get filename from URL path
    if path and '/' in path:
        filename = path.split('/')[-1]
        if filename and '.' in filename:
            return filename
    
    # If no filename in URL, generate one with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"image_{timestamp}.jpg"

def is_valid_image_url(url):
    """Check if the URL might point to an image"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()
    return any(path.endswith(ext) for ext in image_extensions)

def download_image(url, directory="Fetched_Images"):
    """Download image from URL and save to directory"""
    if not url.startswith(('http://', 'https://')):
        print("✗ Invalid URL: Must start with http:// or https://")
        return False
    
    if not is_valid_image_url(url):
        print("⚠ Warning: URL doesn't appear to point to an image file")
        print("Proceeding anyway...")
    
    try:
        print(f"🔗 Connecting to: {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Check if content is actually an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print("⚠ Warning: Server response doesn't appear to be an image")
            print(f"Content-Type: {content_type}")
        
        # Get filename
        content_disposition = response.headers.get('content-disposition', '')
        if 'filename=' in content_disposition:
            # Extract filename from content-disposition header
            filename = content_disposition.split('filename=')[-1].strip('"\'')
        else:
            # Extract from URL or generate
            filename = extract_filename_from_url(url)
        
        # Ensure filename has proper extension
        if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']):
            # Try to determine extension from content-type
            ext = mimetypes.guess_extension(content_type.split(';')[0])
            if ext:
                filename += ext
            else:
                filename += '.jpg'  # default extension
        
        filepath = os.path.join(directory, filename)
        
        # Handle duplicate filenames
        counter = 1
        base_name, extension = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base_name}_{counter}{extension}"
            filepath = os.path.join(directory, filename)
            counter += 1
        
        # Download and save the image
        print(f"📥 Downloading: {filename}")
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        
        file_size = os.path.getsize(filepath)
        print(f"✅ Successfully saved: {filename} ({file_size} bytes)")
        print(f"📁 Location: {os.path.abspath(filepath)}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        print("✗ Connection Error: Unable to connect to the server")
    except requests.exceptions.Timeout:
        print("✗ Timeout Error: Request took too long")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error: {e}")
    except PermissionError:
        print("✗ Permission denied: Cannot write to file")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    return False

def main():
    """Main function"""
    print("=" * 50)
    print("🖼️  Image Fetcher - Ubuntu Principles Edition")
    print("=" * 50)
    print("Community: Connecting to the wider web")
    print("Respect: Graceful error handling")
    print("Sharing: Organized image storage")
    print("Practicality: Real-world utility")
    print("=" * 50)
    
    # Create directory
    directory = create_directory()
    if not directory:
        return
    
    # Get URL from user
    try:
        url = input("🌐 Please enter the image URL: ").strip()
        
        if not url:
            print("✗ No URL provided. Exiting.")
            return
        
        # Download the image
        success = download_image(url, directory)
        
        if success:
            print("🎉 Download completed successfully!")
        else:
            print("❌ Download failed. Please check the URL and try again.")
            
    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user. Goodbye!")
    except EOFError:
        print("\n\n👋 No input provided. Exiting.")

if __name__ == "__main__":
    main()
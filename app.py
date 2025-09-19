"""
Ubuntu-Inspired Image Fetcher Assignment
----------------------------------------

The Wisdom of Ubuntu: "I am because we are."

In the spirit of community and respect, this program mindfully fetches images 
from the internet, checks them for safety, and organizes them for sharing.

Features:
- Handle multiple URLs at once
- Warns if downloading from unsafe or unknown sources
- Prevents duplicate images using SHA-256 hashing
- Checks HTTP headers before saving content
- Fixes missing file extensions automatically
- Developed by Godsfavour Abrahams & Buddy G
"""

import requests
import os
from urllib.parse import urlparse
from hashlib import sha256

# Directory to store images
SAVE_DIR = "Fetched_Images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Track downloaded file hashes to avoid duplicates
downloaded_hashes = set()

def sanitize_url(url: str) -> str:
    """Ensure URL is usable and add https:// if missing"""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def is_valid_image(response) -> bool:
    """Check HTTP headers to ensure the response is an image"""
    content_type = response.headers.get("Content-Type", "")
    return content_type.startswith("image/")

def add_extension_if_missing(filename: str, response) -> str:
    """Append proper file extension if missing"""
    name, ext = os.path.splitext(filename)
    if ext:  # Already has extension
        return filename

    content_type = response.headers.get("Content-Type", "")
    if "jpeg" in content_type:
        return filename + ".jpg"
    elif "png" in content_type:
        return filename + ".png"
    elif "gif" in content_type:
        return filename + ".gif"
    else:
        return filename + ".img"  # fallback if unknown

def download_image(url: str):
    try:
        url = sanitize_url(url)
        parsed_url = urlparse(url)

        # Precaution: Warn if URL is not HTTPS
        if not url.startswith("https://"):
            print(f"⚠️ Warning: {url} is not using HTTPS. Proceed with caution.")

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Check if response is a valid image
        if not is_valid_image(response):
            print(f"✗ Skipped {url} (Content-Type not image/*)")
            return

        # Precaution: Check Content-Length if available
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > 10_000_000:  # >10MB
            print(f"⚠️ Skipped {url} (File too large)")
            return

        # Prevent duplicates by hashing content
        file_hash = sha256(response.content).hexdigest()
        if file_hash in downloaded_hashes:
            print(f"✗ Skipped {url} (Duplicate image)")
            return
        downloaded_hashes.add(file_hash)

        # Extract filename
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image"

        # Fix missing extension
        filename = add_extension_if_missing(filename, response)

        # Save file
        filepath = os.path.join(SAVE_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
    except Exception as e:
        print(f"✗ Unexpected error for {url}: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get multiple URLs from user
    urls = input("Please enter one or more image URLs (separated by commas): ").split(",")

    for url in urls:
        if url.strip():
            download_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
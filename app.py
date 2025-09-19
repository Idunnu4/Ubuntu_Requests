import requests
import os
from urllib.parse import urlparse

MAX_FILE_SIZE = 10 * 1024 * 1024

def fetch_image(url):
    try:
        # Fetch timeout set to 10 seconds
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()  # Raise error for HTTP issues

        # Check content type header
        content_type = response.headers.get('Content-Type', "")
        if not content_type.startswith("image/"):
            print(f"X Skipped (no image) {url}")
            return

        # Check Content Length (file size)
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_FILE_SIZE:
            print(f"X Skipped (file too large) {url}")
            
        # Extract filename from URL or generate one
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        # Prevent overwriting existing files
        filepath = os.path.join("Fetched_Images", filename)
        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(filepath):
            filepath = f"{base}({counter}){ext}"
            counter += 1

         # Save the image
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        # Confirm successful fetch
        print(f"✓ Successfully fetched: {os.path.basename(filepath)}")
        print(f"✓ Image saved to {filepath}")


    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
            print(f"✗ An error occurred: {e}")
    
def main():
        print("Welcome to the Ubuntu Image Fetcher")
        print("A tool for mindfully collecting images from the web\n")
    
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)
    
        # Ask to get URL from user
        urls = input("Please enter the image URL: ").strip(",")
    
        # Fetch each URL
        for url in [u.strip() for u in urls if u.strip()]:
            fetch_image(url)
    
        print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
     main()

        
import os
import requests
from urllib.parse import urlparse

def download_images(url_list):
    """
    Downloads images from a list of URLs and saves them to the current directory.

    Args:
        url_list (list): A list of image URLs to download.
    """
    if not url_list:
        print("No URLs provided for download.")
        return

    print("Starting image download...")

    count = 1

    for url in url_list:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP error status codes (4xx or 5xx)

            parsed_url = urlparse(url)
            filename = str(count) + 'X' + os.path.basename(parsed_url.path)
            
            # Default filename fallback if none could be extracted from the URL path
            if not filename or filename == f"{count}X":
                filename = f"unnamed_image_{url_list.index(url)}.jpg"
                
            filename = filename.split("?")[0]  # Strip query parameters from the filename string if present

            file_path = os.path.join(".", filename)  # Save in the current working directory

            with open(file_path, 'wb') as image_file:
                for chunk in response.iter_content(chunk_size=8192):  # Download in chunks to handle large files efficiently
                    image_file.write(chunk)
            
            count += 1
            print(f"Image successfully downloaded and saved as: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading image from {url}: {e}")
        except Exception as e:
            print(f"Unexpected error processing {url}: {e}")

    print("\nDownload of all images completed.")

if __name__ == "__main__":
    image_urls = [
        "[https://example.com/image1.jpg](https://example.com/image1.jpg)",
        "[https://example.com/image2.jpg](https://example.com/image2.jpg)"
    ]

    download_images(image_urls)

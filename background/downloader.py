import requests
from bs4 import BeautifulSoup
import os
import threading
from background.logger import Logger

class GettingImages():
    def __init__(self):
        self.logger = Logger()

    def download_image(self, image_url, folder):
        try:
            # Ensure the URL is properly formatted
            if not image_url.startswith('http'):
                image_url = 'https:' + image_url if image_url.startswith('//') else 'https://' + image_url
            
            # Create a valid filename from the URL
            image_name = image_url.split('/')[-1]
            if not image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_name += '.jpg'
            
            full_path = os.path.join(folder, image_name)
            self.logger.info(f"Downloading image from: {image_url}")
            self.logger.info(f"Saving to: {full_path}")
            
            response = requests.get(image_url, stream=True)
            self.logger.debug(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                with open(full_path, 'wb') as handler:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            handler.write(chunk)
                self.logger.info(f"Successfully downloaded: {full_path}")
                return True
            else:
                self.logger.error(f"Failed to download {image_url}: HTTP {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"Failed to download {image_url}: {e}")
            return False

    def download_card_images(self):
        # URL of the gallery page
        url = 'https://yugipedia.com/wiki/Gallery_of_Yu-Gi-Oh!_The_Duelists_of_the_Roses_cards'

        # Create folder to store images
        if not os.path.exists('card_images'):
            os.makedirs('card_images')
            self.logger.info("Folder created: card_images")

        # Scrape the gallery page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        } 
        response = requests.get(url, headers=headers)
        self.logger.info(f"Page response status: {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            self.logger.info("Searching for card images...")
            
            # Find all image tags directly
            images = soup.find_all('img')
            self.logger.info(f"Found {len(images)} images")
            
            # Create a list to store threads and successful downloads count
            threads = []
            successful_downloads = 0
            
            # Create a lock for thread-safe counting
            download_lock = threading.Lock()
            
            def download_with_counter(image_url, folder):
                nonlocal successful_downloads
                if self.download_image(image_url, folder):
                    with download_lock:
                        nonlocal successful_downloads
                        successful_downloads += 1
            
            # Process each image
            for img in images:
                if 'src' in img.attrs:
                    original_url = img['src']
                    self.logger.debug(f"Original image URL: {original_url}")
                    
                    # Keep the original URL if it doesn't need transformation
                    image_url = original_url
                    
                    # Only transform URLs that are thumbnails
                    if '/thumb/' in image_url:
                        try:
                            # Keep the URL as is, just ensure it has https:
                            if image_url.startswith('//'):
                                image_url = 'https:' + image_url
                            self.logger.debug(f"Transformed URL: {image_url}")
                            
                            # Only download if it looks like a card image
                            if any(term in image_url.lower() for term in ['cards', 'card_images', '.jpg', '.png']):
                                thread = threading.Thread(
                                    target=download_with_counter,
                                    args=(image_url, 'card_images')
                                )
                                threads.append(thread)
                                thread.start()
                        except Exception as e:
                            self.logger.error(f"Error processing URL {image_url}: {e}")
            
            self.logger.info(f"Started {len(threads)} download threads...")
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            self.logger.info(f"Download complete. Successfully downloaded {successful_downloads} images.")
            return self.logger.get_log_dir()
        else:
            self.logger.error(f"Failed to access the page: HTTP {response.status_code}")
            return None

if __name__ == "__main__":
    downloader = GettingImages()
    log_dir = downloader.download_card_images()
    print(f"\nLogs are available in: {log_dir}")

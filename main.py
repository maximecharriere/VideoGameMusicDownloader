import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
import time
import re
import sys
import argparse

BASE_URL = "https://downloads.khinsider.com"
DOWNLOAD_DELAY = 0  # Delay in seconds between downloads

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

class AlbumInfo:
    def __init__(self, soup):
        self.soup = soup
        self.name = None
        self.year = None
        self.title = None
        self.safe_dirname = None
        self._extract_info()
    
    def _extract_info(self):
        # Try to get info from info file first
        info_link = self.soup.select_one("a i.txt_info_file")
        if info_link and info_link.find_parent("a"):
            self._extract_from_info_file(info_link.find_parent("a")["href"])
        
        # If we couldn't get the info from file, try webpage
        if not self.name:
            self._extract_from_webpage()
        
        # Stop if the name "Ooops!" is found (means the album is not available)
        if self.name == "Ooops!":
            raise ValueError("Album not available")
        
        # Create title
        if self.name and self.year:
            self.title = f"{self.name} ({self.year})"
        elif self.name:
            self.title = self.name
        else:
            self.title = "Unknown Album"
            
        # Make safe for filesystem
        self.safe_dirname = self._make_safe_dirname(self.title)
    
    def _extract_from_info_file(self, info_url):
        try:
            response = requests.get(info_url, headers=HEADERS)
            response.raise_for_status()
            info = response.text
            
            for line in info.split("\n"):
                if line.startswith("Name:"):
                    self.name = line.split("Name:", 1)[1].strip()
                elif line.startswith("Year:"):
                    self.year = line.split("Year:", 1)[1].strip()
        except Exception as e:
            print(f"Error extracting info from info file: {str(e)}")
    
    def _extract_from_webpage(self):
        # Get main title from h2
        title_element = self.soup.select_one("h2")
        if title_element:
            self.name = title_element.text.strip()
        
        # Get year from dedicated field
        year_text = self.soup.find(string="Year:")
        if year_text:
            # Get the text after "Year:" up to the next <br>
            year_sibling = year_text.next_sibling
            if year_sibling:
                # Remove any HTML tags and strip whitespace
                self.year = ''.join(year_sibling.stripped_strings)

    def _make_safe_dirname(self, name):
        # Replace invalid characters with underscore
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove trailing spaces and periods
        safe_name = safe_name.rstrip('. ')
        return safe_name
    
def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def format_size(size_bytes):
    """Convert bytes to human readable string"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def download_file(url, rootdirectory, subdirectory=None, filename=None):
    response = requests.get(url, headers=HEADERS, stream=True)
    response.raise_for_status()
    
    if filename is None:
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = unquote(url.split('/')[-1])
    
    target_dir = rootdirectory
    
    # Handle subdirectory
    if subdirectory:
        target_dir = os.path.join(rootdirectory, subdirectory)
        
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    download_path = os.path.join(target_dir, filename)
    
    if os.path.exists(download_path):
        print(f"Warning: File already exists and will be skipped: {filename}")
        return
    
    # Get total file size
    total_size = int(response.headers.get('content-length', 0))
    formatted_size = format_size(total_size)
    
    # Initialize progress variables
    block_size = 8192
    downloaded = 0
    
    print(f"Downloading: {filename} ({formatted_size})", end='', flush=True)
    
    with open(download_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=block_size):
            downloaded += len(chunk)
            file.write(chunk)
            
            # Calculate progress
            if total_size > 0:  # Avoid division by zero
                progress = (downloaded / total_size) * 100
                status = f"\rDownloading: {filename} ({formatted_size}) [{progress:6.2f}%]"
                sys.stdout.write(status)
                sys.stdout.flush()
    
    sys.stdout.write(f"\rDownloaded: {filename} ({formatted_size}) [100.00%]\n")
    sys.stdout.flush()
    time.sleep(DOWNLOAD_DELAY)

def download_info_file(soup, directory='downloads'):
    info_link = soup.select_one("a i.txt_info_file")
    if info_link and info_link.find_parent("a"):
        info_url = info_link.find_parent("a")["href"]
        try:
            download_file(info_url, filename="info.txt", rootdirectory=directory)
        except Exception as e:
            print(f"Error downloading info file: {str(e)}")
    else:
        print("No info file found for this album")

def download_album_images(soup, directory='downloads'):
    image_links = soup.select("div.albumImage a")
    if not image_links:
        print("No album images found")
        return

    print(f"Found {len(image_links)} album images")
    for link in image_links:
        image_url = link["href"]
        try:
            download_file(image_url, subdirectory="images", rootdirectory=directory)
        except Exception as e:
            print(f"Error downloading image {image_url}: {str(e)}")

def download_tracks(soup, directory='downloads'):
    track_links = soup.select("table#songlist td.playlistDownloadSong a")
    if not track_links:
        print("No tracks found")
        return
    
    print(f"Found {len(track_links)} tracks")
    for link in track_links:
        track_page_url = BASE_URL + link["href"]
        print(f"\nProcessing track: {track_page_url}")
        try:
            soup = get_soup(track_page_url)
            download_links = soup.select("a span.songDownloadLink")
            
            for download_link in download_links:
                file_url = download_link.find_parent("a")["href"]
                try:
                    download_file(file_url, rootdirectory=directory)
                except Exception as e:
                    print(f"Error downloading {file_url}: {str(e)}")
        except Exception as e:
            print(f"Error downloading track {track_page_url}: {str(e)}")

def scrape_album(album_url):
    soup = get_soup(album_url)
    album_info = AlbumInfo(soup)
    
    print(f"Downloading album: {album_info.title}")
    
    if not os.path.exists(album_info.safe_dirname):
        os.makedirs(album_info.safe_dirname)
    
    # Download info file first
    download_info_file(soup, directory=album_info.safe_dirname)
    
    # Download album images
    download_album_images(soup, directory=album_info.safe_dirname)
    
    # Download tracks
    download_tracks(soup, directory=album_info.safe_dirname)

def validate_album_url(url):
    """Validate that the URL is a khinsider album URL"""
    try:
        parsed = urlparse(url)
        base_parsed = urlparse(BASE_URL)
        if parsed.netloc != base_parsed.netloc:
            raise ValueError(f"URL must be from {base_parsed.netloc}")
        if not parsed.path.startswith('/game-soundtracks/album/'):
            raise ValueError("URL must be an album URL (/game-soundtracks/album/...)")
        return url
    except Exception:
        raise ValueError("Invalid URL format")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download music albums from the khinsider "Video Game Music" website.')
    parser.add_argument('album_url', type=validate_album_url,
                      help=f'The URL of the album to download (e.g., {BASE_URL}/game-soundtracks/album/album-name)')
    
    try:
        args = parser.parse_args()
        scrape_album(args.album_url)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

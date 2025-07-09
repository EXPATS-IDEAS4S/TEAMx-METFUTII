import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

BASE_URL = "https://gws-access.jasmin.ac.uk/public/team_x/quicklooks/ACTA/"
LOCAL_BASE_DIR = "/work/dcorradi/teamx/quicklooks/"

def get_links(url):
    """Return list of hrefs from a directory listing."""
    print(f"Accessing: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to access {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = [a.get('href') for a in soup.find_all('a')]
    return [l for l in links if l not in (None, "../", "./")]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def download_file(url, dest):
    """Download a file from `url` to `dest` if not already present."""
    if os.path.exists(dest):
        print(f"Skipping existing file: {dest}")
        return
    print(f"Downloading {url} -> {dest}")
    r = requests.get(url)
    with open(dest, 'wb') as f:
        f.write(r.content)

def extract_date_from_filename(filename):
    """Extract YYYYMMDD from filename like 'bozen_DA10-5_KIT-IMKTRO_20250524_abs.jpg'."""
    match = re.search(r'_(\d{8})_', filename)
    return match.group(1) if match else None

def crawl_and_download(base_url, local_base):
    locations = get_links(base_url)

    for location in locations:
        if not location.endswith("/"):
            continue  # skip files at top level, if any

        location_name = location.strip("/")
        location_url = urljoin(base_url, location)
        instruments = get_links(location_url)

        print(f"\n[+] Processing location: {location_name}")

        for instrument in instruments:
            if not instrument.endswith("/"):
                continue  # skip files, just process folders

            instrument_url = urljoin(location_url, instrument)
            files = get_links(instrument_url)

            print(f"  └─ Instrument: {instrument.strip('/')}, Files: {len(files)}")

            for filename in files:
                if not filename.endswith(".jpg"):
                    continue

                full_file_url = urljoin(instrument_url, filename)
                date_str = extract_date_from_filename(filename)
                if not date_str:
                    print(f"    [!] Could not extract date from: {filename}")
                    continue

                local_dir = os.path.join(local_base, location_name, date_str)
                ensure_dir(local_dir)
                local_path = os.path.join(local_dir, filename)

                download_file(full_file_url, local_path)

if __name__ == "__main__":
    crawl_and_download(BASE_URL, LOCAL_BASE_DIR)

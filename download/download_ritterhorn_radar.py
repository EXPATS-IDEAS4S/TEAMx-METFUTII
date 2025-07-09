import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "https://gws-access.jasmin.ac.uk/public/team_x/quicklooks/ACTA/rittner_horn/Meteor50DX-143/"
LOCAL_DIR = "/data/obs/campaigns/teamx/quicklooks/rittner_horn/"
START_DATE = datetime.strptime("20250501", "%Y%m%d")

def get_links(url):
    print(f"Accessing: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to access {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    links = [a.get('href') for a in soup.find_all('a')]
    return [l for l in links if l and not l.startswith('?') and l != '../']

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def download_file(url, dest):
    if os.path.exists(dest):
        print(f"Skipping existing file: {dest}")
        return
    print(f"Downloading {url} -> {dest}")
    r = requests.get(url)
    if r.status_code == 200:
        with open(dest, 'wb') as f:
            f.write(r.content)
    else:
        print(f"Failed to download: {url} (status code {r.status_code})")

def rename_file(original_filename):
    """
    From: rittner_horn_Meteor50DX-143_KIT-IMKTRO_202411081038.png
    To:   rittner_horn_cd_Meteor50DX-143_KIT-IMTRO_202411081038.png
    """
    match = re.match(r"(rittner_horn)_Meteor50DX-143_KIT-IMKTRO_(\d{12})\.png", original_filename)
    if match:
        timestamp = match.group(2)
        return f"rittner_horn_cd_Meteor50DX-143_KIT-IMKTRO_{timestamp}.png"
    return None  # Skip if filename doesn't match

def crawl_and_download(base_url, local_dir, start_date):
    ensure_dir(local_dir)
    subfolders = get_links(base_url)

    # Normalize existing folders
    downloaded_folders = {
        f[:4] + '-' + f[4:6] + '-' + f[6:8]
        for f in os.listdir(local_dir)
        if os.path.isdir(os.path.join(local_dir, f)) and len(f) == 8 and f.isdigit()
    }

    for folder in subfolders:
        folder = folder.strip('/')  # Remove trailing slash

        # ✅ Only process folders that match YYYY-MM-DD format
        try:
            folder_date = datetime.strptime(folder, "%Y-%m-%d")
        except ValueError:
            print(f"⚠️ Skipping folder with unexpected format: {folder}/")
            continue

        # ✅ Compare datetime objects
        if folder_date < start_date:
            print(f"⏩ Skipping {folder}, before start date.")
            continue

        if folder in downloaded_folders:
            print(f"✅ Skipping already downloaded folder: {folder}/")
            continue

        print(f"\n📁 Processing folder: {folder}/")
        folder_url = urljoin(base_url, folder + "/")
        local_folder_name = folder.replace("-", "")  # Convert to 'YYYYMMDD'
        local_subdir = os.path.join(local_dir, local_folder_name)
        ensure_dir(local_subdir)

        existing_files = set(os.listdir(local_subdir))
        files = get_links(folder_url)

        for f in files:
            if "rittner_horn_Meteor50DX-143_KIT-IMKTRO_" in f and f.endswith(".png"):
                renamed = rename_file(f)
                if renamed is None:
                    print(f"⚠️ Skipping unexpected filename format: {f}")
                    continue

                if renamed in existing_files:
                    print(f"🟡 Already downloaded: {renamed}")
                    continue

                file_url = urljoin(folder_url, f)
                dest_path = os.path.join(local_subdir, renamed)
                print(f"⬇️ Downloading {renamed} from {file_url}")
                download_file(file_url, dest_path)


if __name__ == "__main__":
    crawl_and_download(BASE_URL, LOCAL_DIR, START_DATE)

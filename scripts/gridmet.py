import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

features = ["vpd", "tmmx", "vs", "rmin", "pr"]
years = range(2018, 2025)
os.makedirs("data/raw/gridmet", exist_ok=True)


def download_file(feat, year):
    filename = f"{feat}_{year}.nc"
    url = f"https://www.northwestknowledge.net/metdata/data/{filename}"
    filepath = f"ncdf/{filename}"

    if os.path.exists(filepath):
        print(f"Already exists: {filename}")
        return f"Already exists: {filename}"

    print(f"Starting: {filename}")

    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        downloaded = 0

        with open(filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                f.write(chunk)
                downloaded += len(chunk)
                mb = downloaded / (1024 * 1024)
                print(f"{filename}: {mb:.1f} MB", end="\r")

        print(f"Done: {filename} ({downloaded / (1024 * 1024):.1f} MB)")
        return f"Done: {filename}"

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"Failed: {filename} — {e}")
        return f"Failed: {filename} — {e}"


tasks = [(feat, year) for feat in features for year in years]

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {
        executor.submit(download_file, feat, year): (feat, year) for feat, year in tasks
    }

    for future in as_completed(futures):
        pass  # printing happens inside function now

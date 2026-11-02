import argparse
import hashlib
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
RELEASE_URL = (
    "https://github.com/ber2/2026-esade-pds-course-materials/releases/download/olist-v1/olist-data.zip"
)
EXPECTED_SHA256 = "bfaf064c3c0b09c388b6ad282b4369ff0850cbd083d33931a2e08274fb6cbbb2"
EXPECTED_FILES = [
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]
CHUNK_BYTES = 1024 * 1024


def parse_arguments():
    parser = argparse.ArgumentParser(description="Download the Olist data into data/raw/.")
    parser.add_argument("--force", action="store_true", help="download again even if the files are there")
    parser.add_argument("--url", default=RELEASE_URL, help="where to download the zip from")
    return parser.parse_args()


def data_already_present():
    return all((RAW_DIR / name).is_file() for name in EXPECTED_FILES)


def download(url, destination):
    print(f"Downloading {url}")
    try:
        with urllib.request.urlopen(url) as response, open(destination, "wb") as output:
            total_bytes = int(response.headers.get("Content-Length") or 0)
            received_bytes = 0
            while chunk := response.read(CHUNK_BYTES):
                output.write(chunk)
                received_bytes += len(chunk)
                if total_bytes:
                    print(f"\r  {received_bytes / total_bytes:6.1%} of {total_bytes / 1e6:.0f} MB", end="", flush=True)
        print()
    except urllib.error.URLError as error:
        sys.exit(
            f"\nThe download failed: {error}.\n"
            "Check your internet connection and run the script again.\n"
            "If it keeps failing, download olist-data.zip from the repository's Releases page in your browser\n"
            f"and unzip it into {RAW_DIR}"
        )


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        while chunk := file.read(CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def extract(archive_path):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive_path) as archive:
        for name in archive.namelist():
            with archive.open(name) as source, open(RAW_DIR / Path(name).name, "wb") as target:
                shutil.copyfileobj(source, target)
            print(f"  data/raw/{Path(name).name}")


def main():
    arguments = parse_arguments()
    if data_already_present() and not arguments.force:
        print(f"The Olist data is already in {RAW_DIR}. Nothing to do (use --force to download again).")
        return
    with tempfile.TemporaryDirectory() as temporary_folder:
        archive_path = Path(temporary_folder) / "olist-data.zip"
        download(arguments.url, archive_path)
        actual_sha256 = sha256_of(archive_path)
        if actual_sha256 != EXPECTED_SHA256:
            sys.exit(
                "The downloaded file is not the expected one (checksum mismatch). "
                "It may be incomplete: run the script again."
            )
        print("Checksum OK. Extracting:")
        extract(archive_path)
    print("Done. Next: python scripts/check_setup.py")


if __name__ == "__main__":
    main()

"""Download the public Myntra sample CSV into data/raw/.

Run from the repository root:
    python scripts/download_sample_data.py

This downloads the source dataset; it does not invent product records.
"""
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DEST = RAW_DIR / "myntra_products.csv"
URL = "https://raw.githubusercontent.com/luminati-io/myntra-dataset-sample/main/Myntra%20products%20.csv"


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    request = Request(URL, headers={"User-Agent": "SmartCart-AI student project dataset downloader"})
    print("Downloading the public Myntra sample dataset...")
    try:
        with urlopen(request, timeout=60) as response, DEST.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                output.write(chunk)
    except Exception:
        if DEST.exists():
            DEST.unlink()
        raise
    size_mb = DEST.stat().st_size / (1024 * 1024)
    print(f"Saved: {DEST}")
    print(f"File size: {size_mb:.2f} MB")
    print("Next: run the data pipeline as described in the README.")


if __name__ == "__main__":
    main()

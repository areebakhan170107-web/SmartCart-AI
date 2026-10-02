"""Download the public Myntra sample CSV into data/raw/.

This helper is also available at scripts/download_sample_data.py.
Run from the repository root:
    python download_sample_data.py
"""
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
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
    print(f"Saved: {DEST}")
    print(f"File size: {DEST.stat().st_size / (1024 * 1024):.2f} MB")
    print("The CSV is downloaded. Run the pipeline using the README instructions.")


if __name__ == "__main__":
    main()

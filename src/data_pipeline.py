"""Clean and combine permitted product CSV files for SmartCart-AI.

Put source files in data/raw, then run:
python -m src.data_pipeline --input-dir data/raw --output-dir data/processed
"""
import argparse
import json
import re
from pathlib import Path
import pandas as pd
from src.category_mapping import infer_category, normalize_platform

ALIASES = {
    "product_id": ["product_id", "id", "asin", "sku", "item_id", "objectid"],
    "platform": ["platform", "store", "website", "site", "marketplace", "source"],
    "category": ["category", "main_category", "product_category", "categories", "department"],
    "subcategory": ["subcategory", "sub_category", "product_type", "type"],
    "brand": ["brand", "manufacturer", "vendor"],
    "product_name": ["product_name", "name", "title", "product", "item_name"],
    "price": ["price", "final_price", "selling_price", "sale_price", "discounted_price", "final price"],
    "rating": ["rating", "stars", "average_rating", "review_rating"],
    "reviews": ["reviews", "review_count", "reviews_count", "rating_count", "number_of_reviews"],
    "description": ["description", "product_description", "details", "features", "specifications"],
    "image_url": ["image_url", "image", "image_link", "thumbnail", "main_image", "images"],
    "product_url": ["product_url", "url", "link", "product_link"],
    "currency": ["currency", "price_currency"],
}
COLS = list(ALIASES)
REVERSE = {re.sub(r"[^a-z0-9]+", "_", alias.lower()).strip("_"): canonical for canonical, aliases in ALIASES.items() for alias in aliases}

def platform_from_filename(name):
    n = name.lower().replace("_", " ").replace("-", " ")
    for alias, canonical in [("reliance digital", "Reliance Digital"), ("reliancedigital", "Reliance Digital"), ("flipkart", "Flipkart"), ("amazon", "Amazon"), ("myntra", "Myntra"), ("ajio", "AJIO"), ("croma", "Croma"), ("nykaa", "Nykaa")]:
        if alias in n:
            return canonical
    return ""

def clean_frame(raw, source_file=""):
    rename = {c: REVERSE[re.sub(r"[^a-z0-9]+", "_", str(c).lower()).strip("_")] for c in raw.columns if re.sub(r"[^a-z0-9]+", "_", str(c).lower()).strip("_") in REVERSE}
    df = raw.rename(columns=rename).copy()
    df = df.loc[:, ~df.columns.duplicated()]
    for col in COLS:
        if col not in df.columns:
            df[col] = pd.NA
    df = df[COLS].copy()
    fallback = platform_from_filename(source_file) if source_file else ""
    if fallback:
        blank = df["platform"].isna() | df["platform"].astype(str).str.strip().isin(["", "nan", "None"])
        df.loc[blank, "platform"] = fallback
    df["platform"] = df["platform"].map(normalize_platform)
    text_cols = ["product_id", "platform", "category", "subcategory", "brand", "product_name", "description", "image_url", "product_url", "currency"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NULL": pd.NA})
    for col in ["price", "rating", "reviews"]:
        val = df[col].astype("string").str.replace(",", "", regex=False).str.replace(r"[^0-9.\-]", "", regex=True)
        df[col] = pd.to_numeric(val, errors="coerce")
    df.loc[df["price"] < 0, "price"] = pd.NA
    df.loc[~df["rating"].between(0, 5), "rating"] = pd.NA
    df.loc[df["reviews"] < 0, "reviews"] = pd.NA
    for idx, row in df.iterrows():
        category = str(row["category"]) if pd.notna(row["category"]) else ""
        if category.lower() not in ["clothing", "laptops", "makeup", "mobiles", "electronics", "shoes"]:
            df.at[idx, "category"] = infer_category(category, row["subcategory"], row["product_name"], row["description"])
        elif category.lower() == "clothing":
            df.at[idx, "category"] = "Clothing"
        else:
            df.at[idx, "category"] = category.title()
    df["category"] = df["category"].replace({"Laptop": "Laptops", "Mobile": "Mobiles"})
    df["source_file"] = Path(source_file).name if source_file else ""
    df = df[df["product_name"].notna() & (df["product_name"].astype(str).str.len() > 0)].copy()
    name = df["product_name"].astype(str).str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
    url = df["product_url"].fillna("").astype(str).str.lower().str.strip()
    df["_key"] = df["platform"].fillna("").astype(str).str.lower() + "|" + name + "|" + url
    return df.drop_duplicates("_key").drop(columns="_key").reset_index(drop=True)

def load_and_clean(input_dir):
    paths = sorted(Path(input_dir).glob("*.csv"))
    if not paths:
        raise FileNotFoundError("No CSV files found in " + str(input_dir) + ". Add source CSVs to data/raw first.")
    frames, details = [], []
    for path in paths:
        raw = pd.read_csv(path, low_memory=False)
        cleaned = clean_frame(raw, path.name)
        frames.append(cleaned)
        details.append({"file": path.name, "rows_read": len(raw), "rows_after_cleaning": len(cleaned), "columns_found": list(raw.columns)})
    combined = pd.concat(frames, ignore_index=True)
    combined["_key"] = combined["platform"].fillna("").astype(str).str.lower() + "|" + combined["product_name"].fillna("").astype(str).str.lower().str.strip() + "|" + combined["product_url"].fillna("").astype(str).str.lower().str.strip()
    before = len(combined)
    combined = combined.drop_duplicates("_key").drop(columns="_key").reset_index(drop=True)
    report = {
        "input_files": details,
        "rows_before_cross_file_deduplication": int(before),
        "rows_in_master_catalogue": int(len(combined)),
        "category_counts": {str(k): int(v) for k, v in combined["category"].value_counts(dropna=False).items()},
        "platform_counts": {str(k): int(v) for k, v in combined["platform"].fillna("Missing").value_counts().items()},
        "missing_values": {str(k): int(v) for k, v in combined.isna().sum().items()},
        "note": "Counts describe only source CSVs actually present in the input folder."
    }
    return combined, report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="data/raw")
    parser.add_argument("--output-dir", default="data/processed")
    args = parser.parse_args()
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    master, report = load_and_clean(args.input_dir)
    master.to_csv(output / "master_products.csv", index=False)
    (output / "data_quality_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {len(master):,} products to {output / 'master_products.csv'}")
    print(f"Saved report to {output / 'data_quality_report.json'}")

if __name__ == "__main__":
    main()

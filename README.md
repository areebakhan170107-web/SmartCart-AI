# SmartCart-AI

A Data Science and Machine Learning project for product discovery and personalized recommendations across multiple shopping platforms, featuring product data preprocessing, exploratory data analysis, dynamic filtering, and recommendation algorithms.

## Member 1: data pipeline and catalogue interface

Includes CSV cleaning, a shared product schema, category/retailer mapping, dynamic filters, a Streamlit catalogue interface, tests, and data-source notes.

### Planned category/store workflow
- Clothing: Amazon, Flipkart, Myntra, AJIO
- Laptops: Amazon, Flipkart, Croma, Reliance Digital
- Makeup: Amazon, Flipkart, Nykaa, Myntra
- Mobiles: Amazon, Flipkart, Croma, Reliance Digital
- Electronics: Amazon, Flipkart, Croma, Reliance Digital
- Shoes: Amazon, Flipkart, Myntra, AJIO

**Data status:** The store list is the intended UI workflow, not proof that product data exists for every store. This repository does not yet contain a verified catalogue for all 24 category-store combinations. Do not describe static sample prices as live prices or relabel one retailer's records as another retailer's. See [data/README.md](data/README.md).

## Run locally
```bash
python -m pip install -r requirements.txt
# Put permitted CSVs in data/raw/
python -m src.data_pipeline --input-dir data/raw --output-dir data/processed
streamlit run app.py
```

Run tests with `python -m pytest`. The pipeline generates `data/processed/master_products.csv` and `data/processed/data_quality_report.json` from the real files in `data/raw/`.

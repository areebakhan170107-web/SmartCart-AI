# SmartCart-AI

A Data Science and Machine Learning project for product discovery and personalized recommendations across multiple shopping platforms, featuring product data preprocessing, exploratory data analysis, dynamic filtering, and recommendation algorithms.

## Member 1: product data pipeline

This repository includes category/platform mapping, a CSV cleaning pipeline, dynamic filtering helpers, and unit tests. It accepts permitted CSV datasets in data/raw and generates a standardized master catalogue and data-quality report.

### Categories and store workflow
- Clothing: Amazon, Flipkart, Myntra, AJIO
- Laptops: Amazon, Flipkart, Croma, Reliance Digital
- Makeup: Amazon, Flipkart, Nykaa, Myntra
- Mobiles: Amazon, Flipkart, Croma, Reliance Digital
- Electronics: Amazon, Flipkart, Croma, Reliance Digital
- Shoes: Amazon, Flipkart, Myntra, AJIO

The store list is the intended UI workflow, not proof that data for every retailer is already available. The repository does not yet include a verified complete dataset for all 24 category-store combinations. See data/README.md for source candidates and limitations.

## Run locally
1. Install: python -m pip install -r requirements.txt
2. Put permitted source CSVs in data/raw.
3. Run: python -m src.data_pipeline --input-dir data/raw --output-dir data/processed
4. Test: python -m pytest

The pipeline produces data/processed/master_products.csv and data/processed/data_quality_report.json. Missing data is not fabricated, and static dataset prices should not be described as live.

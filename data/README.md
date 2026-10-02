# Dataset plan and ingestion

Status: the cleaning pipeline is prepared, but no real product CSVs have yet been ingested into this repository. Do not treat the target store matrix as proof that every store has source data.

Public starting points to inspect:
- Multi-store EDA sample project: https://github.com/Narmada-v/E-commerce-Product-Analysis-Project (described as Amazon, Flipkart, eBay; verify actual files and license before use).
- E-commerce sample CSVs: https://github.com/luminati-io/eCommerce-dataset-samples (documents product title, description, prices, ratings, category, brand, image URL and product URL; not all SmartCart stores).
- Amazon Reviews 2023 metadata: https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 (large Amazon-only collection; select product metadata, not huge review files).

SmartCart store workflow:
- Clothing: Amazon, Flipkart, Myntra, AJIO
- Laptops: Amazon, Flipkart, Croma, Reliance Digital
- Makeup: Amazon, Flipkart, Nykaa, Myntra
- Mobiles: Amazon, Flipkart, Croma, Reliance Digital
- Electronics: Amazon, Flipkart, Croma, Reliance Digital
- Shoes: Amazon, Flipkart, Myntra, AJIO

Only identify a row's platform when the source file or listing URL supports it. Never relabel one retailer's product as another retailer's listing. Static dataset prices are not live. Keep original CSVs in data/raw; the pipeline creates data/processed/master_products.csv and a JSON quality report.

Run:
python -m pip install -r requirements.txt
python -m src.data_pipeline --input-dir data/raw --output-dir data/processed

# Dataset plan and ingestion

## Dataset links supplied for SmartCart-AI

These sources are recorded for Member 1's data collection work. A product page describing a dataset is not the same as having its downloadable file in this repository. Paid sources require a purchase/download by an account holder; I will not claim that their files have been ingested until the actual files are available.

1. **Myntra products — Kaggle**  
   https://www.kaggle.com/datasets/ronakbokaria/myntra-products-dataset  
   Intended use: Clothing and shoes from Myntra. Check the dataset's current download files, columns, update date, and license on Kaggle before use. The same URL was shared twice; it is one source, not two datasets.

2. **Croma India product dataset — Actowiz Solutions**  
   https://www.actowizsolutions.com/datasets/details/croma-india-product-dataset  
   The listing advertises product/category/brand/price/MRP/rating/availability/URL fields and shows a paid dataset with a sample preview. The listed price and coverage may change; inspect the sample and terms before buying.

3. **Reliance Digital product dataset — RetailScrape**  
   https://www.retailscrape.com/reliance-digital-ecommerce-product-datasets.php  
   The listing advertises a CSV with product names, prices, ratings, categories, seller/brand details, descriptions, availability and reviews. It displays a paid offering; inspect its sample, license, exact scope and price before purchase.

4. **Nykaa products — Crawl Feeds**  
   https://crawlfeeds.com/datasets/nykaa-products-dataset  
   The listing describes approximately 56,000 beauty/personal-care records in JSON with titles, descriptions, price, images, ratings, reviews, seller/manufacturer information, stock status and product URL. Its stated collection date is July 2021, so treat it as historical/sample data rather than live pricing. The listing displays a paid one-time purchase; verify current price and terms before buying.

## Other potential public sources to assess

- Multi-store EDA sample project: https://github.com/Narmada-v/E-commerce-Product-Analysis-Project (described as Amazon, Flipkart and eBay; inspect actual files and license).
- E-commerce sample CSVs: https://github.com/luminati-io/eCommerce-dataset-samples (inspect actual columns and usage terms).
- Amazon Reviews 2023 metadata: https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023 (large Amazon-only collection; select product metadata rather than large review files).

## SmartCart store workflow

- Clothing: Amazon, Flipkart, Myntra, AJIO
- Laptops: Amazon, Flipkart, Croma, Reliance Digital
- Makeup: Amazon, Flipkart, Nykaa, Myntra
- Mobiles: Amazon, Flipkart, Croma, Reliance Digital
- Electronics: Amazon, Flipkart, Croma, Reliance Digital
- Shoes: Amazon, Flipkart, Myntra, AJIO

This table describes the planned user interface; it does not prove that each retailer/category dataset is present. Do not relabel one retailer's data as another retailer's listing. Do not describe old/static data as live prices or live stock. Preserve source file and capture-date metadata when available. Review each dataset's license/terms before committing it publicly.

## Data ingestion

Place the original permitted CSVs in `data/raw/`. The current pipeline accepts CSV files; a JSON source such as the Crawl Feeds Nykaa file must first be converted to CSV or the pipeline extended to read JSON. The pipeline creates `data/processed/master_products.csv` and `data/processed/data_quality_report.json` based only on actual files present.

Run:
```bash
python -m pip install -r requirements.txt
python -m src.data_pipeline --input-dir data/raw --output-dir data/processed
```

No actual product dataset is claimed to be ingested merely because a source URL appears in this document.

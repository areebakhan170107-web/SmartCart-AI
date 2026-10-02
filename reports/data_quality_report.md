# Data quality report

Status: pipeline added; dataset ingestion pending.

No raw product CSVs have been committed to data/raw, so row counts, missing values, category counts, and retailer coverage cannot yet be truthfully reported. The pipeline will generate these metrics after actual CSVs are added.

Implemented checks: common column aliases, numeric price/rating/review parsing, invalid values, six-category inference, retailer label preservation, conservative duplicate removal, missing-field reporting, and removal of rows without product names.

Review after ingestion: source license/attribution, category coverage, platform coverage, currency normalization, and image/product URL validity.

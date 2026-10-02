import pandas as pd
from src.data_pipeline import clean_frame
from src.filters import available_platforms, filter_products

def test_cleaning_and_category_inference():
    raw = pd.DataFrame([{"title":"Samsung Galaxy S24 smartphone","Website":"AMAZON","Category":"Electronics","Price":"₹ 59,999","Rating":"4.5","Review Count":"120","URL":"https://example.com/p/1"}])
    row = clean_frame(raw, "amazon_products.csv").iloc[0]
    assert row["platform"] == "Amazon"
    assert row["price"] == 59999
    assert row["rating"] == 4.5
    assert row["category"] == "Mobiles"

def test_invalid_rating_becomes_missing():
    row = clean_frame(pd.DataFrame([{"title":"Wireless headphones","store":"Croma","rating":"8"}])).iloc[0]
    assert pd.isna(row["rating"])
    assert row["category"] == "Electronics"

def test_workflow_platforms():
    assert available_platforms("Clothing") == ["Amazon", "Flipkart", "Myntra", "AJIO"]
    assert available_platforms("Makeup") == ["Amazon", "Flipkart", "Nykaa", "Myntra"]

def test_filters():
    data = pd.DataFrame([{"product_name":"Phone A","category":"Mobiles","platform":"Amazon","price":10000,"rating":4.2},{"product_name":"Phone B","category":"Mobiles","platform":"Flipkart","price":20000,"rating":4.7}])
    result = filter_products(data, category="Mobiles", platforms=["Amazon"], max_price=15000)
    assert result["product_name"].tolist() == ["Phone A"]

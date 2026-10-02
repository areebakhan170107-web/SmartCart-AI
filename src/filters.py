"""Reusable filters for SmartCart-AI."""
import pandas as pd
from src.category_mapping import PLATFORMS_BY_CATEGORY

def available_platforms(category):
    return PLATFORMS_BY_CATEGORY.get(category, []).copy()

def filter_products(products, category=None, subcategory=None, platforms=None, min_price=None, max_price=None, brands=None, min_rating=None, query=None):
    result = products.copy()
    if category and "category" in result:
        result = result[result["category"].astype("string").str.casefold() == category.casefold()]
    if subcategory and "subcategory" in result:
        result = result[result["subcategory"].astype("string").str.contains(subcategory, case=False, na=False)]
    if platforms:
        result = result[result["platform"].isin(platforms)]
    if min_price is not None and "price" in result:
        result = result[result["price"].notna() & (result["price"] >= min_price)]
    if max_price is not None and "price" in result:
        result = result[result["price"].notna() & (result["price"] <= max_price)]
    if brands and "brand" in result:
        result = result[result["brand"].isin(brands)]
    if min_rating is not None and "rating" in result:
        result = result[result["rating"].notna() & (result["rating"] >= min_rating)]
    if query:
        cols = [c for c in ["product_name", "brand", "description", "subcategory"] if c in result]
        mask = pd.Series(False, index=result.index)
        for col in cols:
            mask |= result[col].astype("string").str.contains(query, case=False, na=False, regex=False)
        result = result[mask]
    return result.reset_index(drop=True)

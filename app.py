"""Streamlit catalogue browser for SmartCart-AI Member 1."""
from pathlib import Path
import pandas as pd
import streamlit as st
from src.category_mapping import PLATFORMS_BY_CATEGORY
from src.filters import filter_products

st.set_page_config(page_title="SmartCart-AI", page_icon="🛍️", layout="wide")
st.title("🛍️ SmartCart-AI")
st.caption("Explore products by category, store, budget and rating. Dataset prices are not live.")

DATA_PATH = Path("data/processed/master_products.csv")
if not DATA_PATH.exists():
    st.warning("The product catalogue has not been generated yet.")
    st.markdown("Add permitted product CSV files to **data/raw/**, then run:")
    st.code("python -m pip install -r requirements.txt\npython -m src.data_pipeline --input-dir data/raw --output-dir data/processed")
    st.info("The category and retailer menus below show the planned workflow; products will appear after real datasets are processed.")
    st.stop()

products = pd.read_csv(DATA_PATH)
for col in ["category", "platform", "product_name", "brand", "subcategory", "description", "image_url", "product_url"]:
    if col not in products.columns:
        products[col] = pd.NA
for col in ["price", "rating", "reviews"]:
    if col not in products.columns:
        products[col] = pd.NA
    products[col] = pd.to_numeric(products[col], errors="coerce")

categories = list(PLATFORMS_BY_CATEGORY)
category = st.selectbox("1. Choose a category", categories)
allowed = PLATFORMS_BY_CATEGORY[category]
subset = products[products["category"].astype("string").str.casefold() == category.casefold()]
available = [p for p in allowed if p in set(subset["platform"].dropna().astype(str))]
platform_choices = st.multiselect("2. Choose stores", allowed, default=available)
if not available:
    st.caption("No product records for this category/store yet. The menu shows the planned store choices.")
if subset.empty:
    st.warning(f"No dataset records are currently available for **{category}**. Add real CSV data for this category.")
    st.stop()

left, middle, right = st.columns(3)
with left:
    prices = subset["price"].dropna()
    max_available = float(prices.max()) if not prices.empty else 100000.0
    max_price = st.number_input("3. Maximum price (dataset currency)", min_value=0.0, value=max_available, step=500.0)
with middle:
    brand_values = sorted(subset["brand"].dropna().astype(str).unique().tolist())
    brands = st.multiselect("Brand", brand_values)
with right:
    min_rating = st.selectbox("Minimum rating", [0.0, 3.0, 3.5, 4.0, 4.5], index=0)

query = st.text_input("Search products", placeholder="e.g. cotton shirt, laptop, lipstick")
filtered = filter_products(subset, category=category, platforms=platform_choices or [], max_price=max_price, brands=brands or None, min_rating=min_rating if min_rating else None, query=query or None)
st.write(f"**{len(filtered):,} products found**")
if filtered.empty:
    st.info("No products match those filters. Try selecting more stores or increasing the price limit.")
else:
    for start in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, (_, product) in zip(cols, filtered.iloc[start:start + 3].iterrows()):
            with col:
                image_url = product.get("image_url")
                if pd.notna(image_url) and str(image_url).startswith(("https://", "http://")):
                    st.image(str(image_url), use_container_width=True)
                st.subheader(str(product.get("product_name", "Product")))
                st.caption(f"{product.get('brand') if pd.notna(product.get('brand')) else 'Brand not listed'} · {product.get('platform') if pd.notna(product.get('platform')) else 'Store not listed'}")
                price = product.get("price")
                st.write(f"Price: {price:,.2f}" if pd.notna(price) else "Price not available in dataset")
                rating = product.get("rating")
                if pd.notna(rating):
                    st.write(f"⭐ {rating:.1f}/5")
                description = product.get("description")
                if pd.notna(description) and str(description).strip():
                    st.write(str(description)[:180] + ("…" if len(str(description)) > 180 else ""))
                url = product.get("product_url")
                if pd.notna(url) and str(url).startswith(("https://", "http://")):
                    st.link_button("Open original listing", str(url))

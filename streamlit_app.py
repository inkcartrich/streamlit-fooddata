# streamlit_app.py

import streamlit as st
import pandas as pd
from string import capwords

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

#
# Brands
#

selector_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0 AND
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 1
"""

df_selector_raw = conn.query(selector_query, ttl=600)

st.text("Searching " + str(len(df_selector_raw)) + " brand-name products.")

df_brands = df_selector_raw.drop_duplicates("BRAND_OWNER")

brand_selection = st.selectbox(
    "Select or search for a brand:",
    df_brands['BRAND_OWNER'],
    None,
    format_func=lambda x: capwords(x)
)

df_brand_products = df_selector_raw[df_selector_raw['BRAND_OWNER'] == brand_selection]

st.text("Found " + str(len(df_brand_products)) + " products.")

product_selection = st.selectbox(
    "Select or search for a product:",
    df_brand_products['BRAND_NAME'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected brand: {brand_selection}")
st.text(f"Selected product: {product_selection}")
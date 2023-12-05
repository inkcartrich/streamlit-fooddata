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

brand_query = f"""
SELECT DISTINCT BRAND_OWNER from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0 AND
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 1
"""

df_brands = conn.query(brand_query, ttl=600)

st.text("Searching " + str(len(df_brands)) + " brands.")

brand_selection = st.selectbox(
    "Select or search for a brand:",
    df_brands['BRAND_OWNER'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected brand: {brand_selection}")

#
# Products
#

product_query = f"""
SELECT DISTINCT BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER LIKE ANY "{brand_selection}" AND
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 1
"""

df_products = conn.query(product_query, ttl=600)

st.text("Found " + str(len(df_products)) + " products.")

product_selection = st.selectbox(
    "Select or search for a product:",
    df_products['BRAND_NAME'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected product: {product_selection}")

st.write("#")
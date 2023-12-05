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
    GROUP BY BRAND_OWNER
    HAVING COUNT(BRANDED_FOOD.BRAND_NAME) > 1
"""

df_selector = conn.query(selector_query, ttl=600)

st.text("Searching " + str(len(df_selector)) + " products.")

brand_slicer = st.selectbox(
    "Select or search for a brand:",
    df_selector['BRAND_OWNER'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected brand: {brand_slicer}")

#
# Products
#

product_slicer = st.selectbox(
    "Select or search for a brand:",
    df_selector['BRAND_NAME'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected product: {product_slicer}")

st.write("#")
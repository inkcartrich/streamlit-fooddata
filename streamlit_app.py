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
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0 
    GROUP BY BRAND_OWNER
    HAVING COUNT(BRANDED_FOOD.BRAND_NAME) > 1
"""

df_brand = conn.query(brand_query, ttl=600)

st.text("Searching " + str(len(df_brand)) + " brands.")

brand_slicer = st.selectbox(
    "Select or search for a brand:",
    df_brand['BRAND_OWNER'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected brand: {brand_slicer}")

st.write("#")

#
# Products
#

product_query = f"""
SELECT DISTINCT BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER = '{brand_slicer}' AND
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 1
"""

df_products = conn.query(product_query, ttl=600)

st.text("Found " + str(len(df_brand)) + " products.")

product_slicer = st.selectbox(
    "Select or search for a brand:",
    df_products['BRAND_NAME'],
    None,
    format_func=lambda x: capwords(x)
)

st.text(f"Selected product: {product_slicer}")

st.write("#")
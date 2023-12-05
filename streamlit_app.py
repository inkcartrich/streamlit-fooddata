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

st.write("#")

#
# Products
#

df_products = conn.query(brand_query, ttl=600)

st.text("Searching " + str(len(df_brand)) + " brands.")

brand_slicer = st.selectbox(
    "Select or search for a brand:",
    df_brand['BRAND_OWNER'],
    None,
    format_func=lambda x: capwords(x)
)

st.write("#")

#
# Old
#


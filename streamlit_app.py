# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as pd
from string import capwords

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

#
# Brands
#

selector_query = f"""
SELECT DISTINCT BRAND_OWNER, 
        BRAND_NAME,
        INGREDIENTS,
        SERVING_SIZE,
        SERVING_SIZE_UNIT,
        BRANDED_FOOD_CATEGORY,
        PACKAGE_WEIGHT,
        AVAILABLE_DATE
    FROM BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0 AND
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 1 
"""

df_selector = conn.query(selector_query, ttl=600)

st.text("Searching " + str(len(df_selector)) + " brand-name products.")

df_selector['concat'] = df_selector['BRAND_OWNER'] + ' - ' + df_selector['BRAND_NAME'] 

selection = st.selectbox(
    "Select or search for a product:",
    df_selector['concat'],
    None,
    format_func=lambda x: capwords(x)
)

df_selection = df_selector[df_selector['concat'] == selection]

st.dataframe(df_selection)

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
SELECT DISTINCT BRAND_OWNER, BRAND_NAME
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

brand_owner = df_selection['BRAND_OWNER'].iloc[0]
brand_name = df_selection['BRAND_NAME'].iloc[0]

detail_query = f"""
SELECT * FROM BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER = $${brand_owner}$$ AND
    BRANDED_FOOD.BRAND_NAME = $${brand_name}$$ AND
    INGREDIENTS IS NOT NULL AND
    GTIN_UPC IS NOT NULL AND
    SERVING_SIZE IS NOT NULL AND
    SERVING_SIZE_UNIT IS NOT NULL AND
    BRANDED_FOOD_CATEGORY IS NOT NULL AND
    PACKAGE_WEIGHT IS NOT NULL
    LIMIT 1
"""

df_detail = conn.query(detail_query, ttl=600)

st.dataframe(df_detail)

detail_list = df_detail.loc[0].to_dict()

st.write(detail_list)

st.markdown(f"""

"""
)
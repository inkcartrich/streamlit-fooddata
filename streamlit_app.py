# streamlit_app.py

import streamlit as st
import pandas as pd
from string import capwords

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

brand_query = f"""
SELECT DISTINCT BRAND_OWNER from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0
"""

df_brand = conn.query(brand_query, ttl=600)

st.text("Seaching " + str(len(df_brand)) + " brands.")

st.write("#")

suggestions_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME, BRANDED_FOOD_CATEGORY from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) AND 
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND 
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 0 AND
    BRANDED_FOOD.BRAND_OWNER != BRANDED_FOOD.BRAND_NAME
"""

df_suggest = conn.query(suggestions_query, ttl=600)

df_suggest['concat'] = df_suggest['BRAND_OWNER'] + " - " + df_suggest['BRAND_NAME'] + " - " + df_suggest['BRANDED_FOOD_CATEGORY']

st.text("Searching " + str(len(df_suggest)) + " brand-name products.")

st.write("#")

search_brand_name = st.selectbox(
    "Select or search for a brand name",
    df_suggest['concat'],
    None,
    format_func=lambda x: capwords(x)
)

st.write("#")

st.text("Selected product:")

df_selection = df_suggest[df_suggest['concat'] == search_brand_name][['BRAND_OWNER', 'BRAND_NAME']]

selection_owner = df_selection[['BRAND_OWNER']].iloc[0].to_string(index=False)
selection_product = df_selection[['BRAND_NAME']].iloc[0].to_string(index=False)

st.write("Brand Owner: " + selection_owner)
st.write("Product: " + selection_product)

query_detailed_string = f"""
SELECT DISTINCT * from BRANDED_FOOD 
    WHERE 
        BRAND_OWNER = '{selection_owner}' AND BRAND_NAME = UPPER('{selection_product}')
    LIMIT 100;
"""

# Perform query.
df_raw = conn.query(query_detailed_string, ttl=600)

df_display = df_raw[['BRAND_OWNER', 'BRAND_NAME', 'GTIN_UPC', 'INGREDIENTS']]

# Print results.
st.dataframe(df_raw,
            hide_index=True)

# streamlit_app.py

import streamlit as st
import pandas as pd
from string import capwords

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

brands_query = f"""
SELECT DISTINCT BRAND_OWNER from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) > 0 
"""

df_brands = conn.query(brands_query, ttl=600)

st.text("Searching " + str(len(df_brands)) + " brands.")

search_brands = st.selectbox(
    "Select or search for a brand name",
    df_brands,
    None,
    format_func=lambda x: capwords(x)
)

st.text(search_brands)

products_query = f"""
SELECT DISTINCT BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER == {search_brands}
"""

df_products = conn.query(products_query, ttl=600)

st.text("Found " + str(len(df_products)) + " products.")

suggestions_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_OWNER IS NOT NULL AND
    LENGTH(BRANDED_FOOD.BRAND_OWNER) AND 
    BRANDED_FOOD.BRAND_NAME IS NOT NULL AND 
    LENGTH(BRANDED_FOOD.BRAND_NAME) > 0 AND
    BRANDED_FOOD.BRAND_OWNER != BRANDED_FOOD.BRAND_NAME
"""

df_suggest = conn.query(suggestions_query, ttl=600)

df_suggest['concat'] = df_suggest['BRAND_OWNER'] + " - " + df_suggest['BRAND_NAME']

st.text("Searching " + str(len(df_suggest)) + " brand-name products.")

search_brand_name = st.selectbox(
    "Select or search for a brand name",
    df_suggest['concat'],
    None,
    format_func=lambda x: capwords(x)
)

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

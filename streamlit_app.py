# streamlit_app.py

import streamlit as st
import pandas as pd

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

st.subheader("Explore the USDA FoodData Central dataset!")

suggestions_query = f"""
SELECT DISTINCT BRAND_OWNER, BRAND_NAME from BRANDED_FOOD
    WHERE BRANDED_FOOD.BRAND_NAME IS NOT NULL AND LENGTH(BRANDED_FOOD.BRAND_NAME) > 0
    LIMIT 100;
"""

df_suggest = conn.query(suggestions_query, ttl=600)

df_suggest['concat'] = df_suggest['BRAND_OWNER'] + " - " + df_suggest['BRAND_NAME']

st.dataframe(df_suggest,
            hide_index = True)

search_brand_name = st.selectbox(
    "Select or search for a brand name",
    df_suggest['concat'],
    None,
    format_func=lambda x: x.title()
)

st.dataframe(df_suggest[df_suggest['concat'] == search_brand_name],
            hide_index = True)

#Search bar for brand-name foods
query_brand_name = st.text_input(
    "TO BE DROPPED - Search for a brand name",
    "Cocoa puffs"
)

query_string = f"""
SELECT * from BRANDED_FOOD 
    WHERE BRAND_NAME = UPPER('{query_brand_name}')
    LIMIT 100;
"""

# Perform query.
df_raw = conn.query(query_string, ttl=600)

df_display = df_raw[['BRAND_OWNER', 'BRAND_NAME', 'GTIN_UPC', 'INGREDIENTS']]

# Print results.
st.dataframe(df_display,
            hide_index=True)

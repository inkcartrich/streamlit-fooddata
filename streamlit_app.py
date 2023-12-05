# streamlit_app.py

import streamlit as st

# Initialize connection.
conn = st.connection("snowflake")

st.title("USDA FoodData Central")

suggestions_query = f"""
SELECT BRAND_OWNER, BRAND_NAME from BRANDED_FOOD
    WHERE BRAND_NAME IS NOT NULL
    LIMIT 100;
"""

df_suggest = conn.query(suggestions_query, ttl=600)

st.dataframe(df_suggest,
            hide_index = True)

#Search bar for brand-name foods
query_brand_name = st.text_input(
    "Search for a brand name",
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

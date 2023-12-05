# streamlit_app.py

import streamlit as st

# Initialize connection.
conn = st.connection("snowflake")

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
st.dataframe(df_display)

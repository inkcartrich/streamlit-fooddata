# streamlit_app.py

import streamlit as st

# Initialize connection.
conn = st.connection("snowflake")

#Search bar for brand-name foods
query_brand_name = st.text_input(
    "Search for a food product",
    "Cocoa puffs"
)

# Perform query.
#df = conn.query(f'SELECT * from BRANDED_FOOD WHERE BRAND_NAME = "{query_brand_name}";', ttl=600)

# Print results.
df

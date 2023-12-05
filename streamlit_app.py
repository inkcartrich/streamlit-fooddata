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
"""

# Perform query.
df = conn.query(query_string, ttl=600)

# Print results.
df
